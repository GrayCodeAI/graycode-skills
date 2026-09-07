---
name: hpc-slurm-remote-execution
description: "Run compute jobs on a remote Slurm HPC cluster over SSH, discovering partitions, GPUs, and storage instead of assuming."
license: Apache-2.0
tags:
- hpc
- slurm
- remote-execution
- scientific
---

# MIT ORCD Remote Execution

Run work on MIT's ORCD cluster (`orcd-login.mit.edu`, Slurm cluster `eofe7`,
"Engaging") from your own machine over one multiplexed SSH connection. The
scripts run **locally** and reach the cluster over ssh; they do not run *on* a
login node (no `orcd` alias there, and its `python3` is 3.6). Already on the
cluster? Use `sinfo`/`sbatch` and the references directly.

Every number below is a snapshot: trust script output over docs. When answering
a person, lead with the decision (what to run, where, when it starts); evidence
after.

## Start here, every session

Run the scripts by path from any directory; they find each other.

```bash
python3 <skill>/scripts/orcd_doctor.py        # access working? exact fix if not; exit 0 = reachable
python3 <skill>/scripts/orcd_resources.py --gpus --idle   # what you may run on, what is free now
python3 <skill>/scripts/orcd_storage.py       # where data goes, quotas, tiers
python3 <skill>/scripts/orcd_snapshot.py --save           # baseline config; later --diff (exit 2 = drift)
```

## Connection rules

- sshd requires `publickey` **and** `keyboard-interactive` (Duo). Sign in once
  at <https://orcd-ood.mit.edu/>; while that trust holds, ssh is silent. A Duo
  prompt on ssh means it lapsed: sign in again, or run `ssh orcd` by hand. Keys
  are not the problem.
- **Never set `BatchMode=yes`.** It disables keyboard-interactive, so auth
  always fails with `Permission denied (keyboard-interactive)` -- looks like a
  bad key, is not.
- One `ControlMaster` socket (`ControlPersist 12h`) carries the session.
  `orcd_doctor.py --fix` writes the correct `~/.ssh/config` block; use the
  scripts or `ssh orcd`, never hand-rolled flags.
- 10 failed Duo attempts lock the account for 90 min. Close anything that
  auto-reconnects (VS Code Remote-SSH) before retrying.

## First-time setup

No passwords over ssh: the key is installed through the portal
(references/setup.md).

1. `ssh-keygen -t ed25519` (passphrase held in `ssh-agent`).
2. Sign in at <https://orcd-ood.mit.edu/>; **Clusters -> Shell Access**.
3. Append the `.pub` line to `~/.ssh/authorized_keys` there.
4. `python3 orcd_doctor.py --fix --user <mit-username>` (add `--identity <key>`
   if the ORCD key is not the first of `id_ed25519`/`id_ecdsa`/`id_rsa`).

**Cloud or sandbox session** (Claude Code on the web, CI): the key lives in an
ephemeral container, and authorizing it grants that container account access.
Say so. If the doctor's `tcp port 22` check passes, `orcd_doctor.py
--sandbox-setup` mints a dedicated identifiable key and prints the exact
`authorized_keys` command (and its revocation) for the **account owner** to
run -- the agent never adds a key itself. If port 22 is blocked, no key helps;
the environment's network policy must allow ssh egress.

A reachable account may still lack a Slurm association or `orcd_rg_*` storage
groups (the doctor WARNs). Fix: email orcd-help@mit.edu.

## Login nodes are for orchestration, not work

`ssh orcd '<cmd>'` runs on a shared login node. Editing, git, scheduler
queries, quota checks: fine. Anything that computes, compiles, resolves an
environment, unpacks a dataset or checksums a tree: run it in a job.

```bash
ssh orcd 'srun -p mit_quicktest -t 15 -c 4 --mem=8G <cmd>'           # <=15 min, starts ~instantly
ssh orcd -t 'srun -p mit_quicktest -t 15 -n 1 --mem=8G --pty bash'    # interactive shell
```

Longer than 15 min: `ou_*_high` or `mit_normal` with a short `-t`. Large
copies: `mit_data_transfer`. See references/slurm.md.

## Discovering what you can run on

Entitlement is per person (`AllowGroups` plus the partition's own QOS); never
hardcode a partition. `orcd_resources.py` asks the scheduler; `orcd_submit.py
--plan` reports where a real request lands and **when it would start**.

- `sbatch --test-only` is the access oracle but ignores QOS TRES ceilings.
  `--plan` cross-checks the GPU ceilings in `MaxTRESPU` (yours) and `GrpTRES`
  (one pool shared with the whole group) and marks impossible rows `EXCEEDS`;
  CPU/memory ceilings are not checked.
- **Never pass `--qos`** (-> `Invalid qos specification`); the partition
  supplies it.
- **Request GPUs by model**: `--gres=gpu:h100:2`. Untyped may land on an L4 or
  an H200; partitions labelled `untyped` accept only `gpu:N`.

## Storage

| Group prefix -> mount | Tier | Use |
| --- | --- | --- |
| `fstor*` -> `/orcd/scratch`, `/orcd/compute` | flash | job IO |
| `hstor*` -> `/orcd/data`, `/orcd/pool` | capacity | datasets, results |
| `core*` -> `/orcd/archive` | archive | cold data |
| `nfs*` -> `$HOME` | home | code and config only |

- **Only `$HOME` is backed up.** Treat every other tier as unprotected.
- **`$HOME` is the slowest tier and the default cwd.** Job IO and stdout go
  elsewhere: `orcd_submit.py --chdir <flash path> --output '%x-%j.out'`.
- **1 M inode caps** on `~` and `~/orcd/scratch`. Unpacked image sets and venvs
  hit them at a few percent of the byte quota; it presents as "disk full".
  Keep datasets as archives or shards.
- **Two flash scratches.** Personal `~/orcd/scratch` (1 TB): Python
  environments and `UV_CACHE_DIR`. Group `/orcd/scratch/bcs/<NNN>/<user>` (as
  listed by `orcd_storage.py`): runs. Group dirs are group-readable and closed to others --
  `orcd_storage.py --setup` creates yours with `chmod o-rwx`; job scripts start
  with `umask 027`.
- **Symlink forms in anything shared**: `~/orcd/scratch`, resolved at runtime
  with `readlink -f`. `/orcd/scratch/orcd/<NNN>/<user>` shards are per-person.
- Quotas appear only in `~/orcd/.quota` (`df` shows the whole filesystem);
  `orcd_storage.py` reads it.
- Before placing a dataset, ask for file count and access pattern; size alone
  decides nothing.
- Traps: bare `df -h` hangs on a stale mount (use `/proc/mounts` and
  `timeout`); `/orcd` is autofs (listing a parent is not an inventory).

Measured throughput and the stage-in/stage-out pattern:
references/storage.md.

## Group layer: sensein

references/sensein.md with machine-readable
assets/sensein.json, loaded by `orcd_storage.py` (other
groups: `--group-config` or `ORCD_GROUP_CONFIG`). Covers which
`/orcd/data/{satra,dandi,linc}` trees are ours, the WebMoira lists that grant
access, and consolidation: one shared `HF_HOME` with every model **pinned by
commit hash, never a floating `main`**; shared `models/`, `datasets/`,
`cache/<tool>` (senselab); per-user `users/`.

## Python: uv in the cluster `$HOME`

Login-node `python3` is 3.6 and there is no system uv or conda.

```bash
python3 orcd_uv.py             # installed? version? on PATH?
python3 orcd_uv.py --install   # install or upgrade; never edits shell profiles
```

Scripts call `$HOME/.local/bin/uv` by absolute path. **Any shell-profile edit
(`~/.bashrc`, `~/.bash_profile`, `~/.profile`, by hand or by an installer)
needs the user's explicit yes first**; then `orcd_uv.py --add-to-path
--user-approved`. Build environments inside a `mit_quicktest` job on
`~/orcd/scratch/envs` with `UV_CACHE_DIR=$(readlink -f ~/orcd/scratch)/uv-cache`.

## Submitting and tracking

```bash
python3 orcd_submit.py --plan --gpus 1 --gpu-type h100 --cpus 8 --mem 64G --time 2:00:00
python3 orcd_submit.py --script train.sh --gpus 1 --gpu-type h100 --cpus 8 --mem 64G --time 4:00:00 \
    --chdir /orcd/scratch/bcs/<NNN>/<user>/runs --output '%x-%j.out'
python3 orcd_submit.py --queue
python3 orcd_submit.py --status <jobid>
```

- Other flags: `--partition` (pin), `--nodes`, `--array`, `--name`,
  `--wrap '<cmd>'` or `--remote-script <path>` instead of `--script`.
- `--plan` before any long job: partition choice moves start time from minutes
  to days.
- **Always set `--mem`.** Default is 1 GB per CPU; jobs die mid-run.
- **Arrays**: each task is a submitted job. Max array = partition
  `MaxSubmitPU + 1` (`orcd_snapshot.py` prints it); `%K` throttles concurrency
  and does not raise it; the association `MaxSubmit` caps across all
  partitions.
- **Multi-GPU shape**: `-N 1 --gres=gpu:h100:4` = 4 on one node (NVLink);
  `-N 2 --gres=gpu:h100:4` = 8 across nodes (needs a distributed launcher).
  Packed is scarcer -- `--plan` both.
- **Preemptable** (`mit_preemptable`, `ou_*_low`): far more capacity,
  `PreemptMode=REQUEUE`. For checkpointed or idempotent work only: trap
  `--signal=B:USR1@120`, checkpoint, **exit non-zero**.

## When something goes wrong

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Permission denied (keyboard-interactive)` | `BatchMode=yes`, or Duo trust lapsed | Remove BatchMode; sign in at the portal |
| Duo prompts on every ssh | web authorization expired | Sign in at the portal once |
| Connection times out; doctor FAILs `tcp port 22` | network policy blocks ssh egress (cloud sandboxes) | Not a key problem; change the policy or run elsewhere |
| Locked out | 10 failed Duo attempts, 90 min | Stop retrying; close auto-reconnecting clients |
| `Invalid qos specification` | passed `--qos` | Drop it; pick the partition |
| `Requested node configuration is not available` | GPU model absent from partition | `orcd_resources.py --gpus` |
| Job dies mid-run, no clear error | 1 GB/CPU default memory | Set `--mem` |
| `Could not open stdout file` at job start | relative `-o` resolved against `$HOME` | Absolute `-o`, or `--chdir`; dir must exist |
| Job waits for days | congested shared partition | `--plan`; private or preemptable partition |
| Job vanished and requeued | `PreemptMode=REQUEUE` | Expected; checkpoint, or non-preemptable partition |
| `QOSMaxSubmitJobPerUserLimit` | array > `MaxSubmitPU`; `%K` does not help | Arrays of `MaxSubmitPU + 1` or fewer |
| Process killed on the login node / everything slow for everyone | computing on a login node | `srun -p mit_quicktest ...` |
| A command hangs forever | bare `df -h`, stale mount | `/proc/mounts`; `timeout` |
| Everything mysteriously slow | job IO in `$HOME` | Move it to flash scratch |
| Disk full but quota looks fine | 1 M inode limit | File columns in `orcd_storage.py` |
| `uv: command not found` on the cluster | not installed / not on PATH | `orcd_uv.py --install`; absolute path, or approved profile edit |
| Worked last month, fails now | cluster config changed | `orcd_snapshot.py --diff` |

## Scripts

| Script | Purpose |
| --- | --- |
| `orcd_doctor.py` | Verify access with exact remedies. `--fix` writes ssh config; `--sandbox-setup` for cloud sandboxes |
| `orcd_resources.py` | Usable partitions, GPU models, QOS ceilings, live free GPUs |
| `orcd_storage.py` | Writable storage by tier, quotas, group conventions. `--setup` creates locked-down per-user dirs |
| `orcd_uv.py` | Check/install/upgrade uv in the cluster `$HOME`; profile edits only with approval (`--profile` picks the file) |
| `orcd_submit.py` | Plan, submit, track; auto-select partition by start time; `--chdir` |
| `orcd_snapshot.py` | Config snapshot; `--save` baseline, `--diff` drift (exit 2), `--baseline <file>` |
| `orcd_common.py` | Shared ssh plumbing |

Stdlib-only Python 3, run locally. All accept `--host`; discovery scripts
accept `--json`.
