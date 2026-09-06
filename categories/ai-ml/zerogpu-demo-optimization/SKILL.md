---
name: zerogpu-demo-optimization
description: "Write and debug ML demo code for ZeroGPU Spaces: @spaces.GPU decorators, duration and quota tuning, process isolation, CUDA availability, and concurrency-safe patterns."
license: Apache-2.0
tags:
- gpu
- gradio
- ml-demo
- spaces
---

# Hugging Face ZeroGPU

Rules and patterns for ML demos on Hugging Face Spaces with **ZeroGPU** hardware. Covers `@spaces.GPU`, duration and quota tuning, process isolation, the CUDA availability model, concurrency safety, and CUDA build constraints.

## Scope

This skill is for **Gradio SDK Spaces using ZeroGPU hardware**. Docker and Static Spaces cannot schedule onto ZeroGPU, and Streamlit apps now run as Docker Spaces — so this skill applies only to Gradio. For general Gradio coding (components, layouts, event listeners), see the `huggingface-gradio` skill in this repo. The authoritative ZeroGPU docs live at https://huggingface.co/docs/hub/spaces-zerogpu — refer to them for the current backing GPU, runtime version lists, and tier thresholds, all of which change over time.

## Reference Files

| Reference | When to read |
|-----------|--------------|
| `references/concurrency.md` | Always read alongside SKILL.md when writing ZeroGPU code — handlers run in parallel by default |
| `references/how-zerogpu-works.md` | When reasoning about cold-starts, worker reuse, why module-scope warmup does not carry to requests, or why returning CUDA tensors hangs |
| `references/how-quota-works.md` | When choosing `duration` values, debugging `illegal duration` vs `quota exceeded` errors, or explaining why default 60s blocks short tasks |
| `references/cuda-and-deps.md` | When installing CUDA-dependent packages (e.g. `flash-attn`), pinning torch side-cars, or reading wheel filename tags |

## Hardware

ZeroGPU exposes two GPU sizes that map to a fraction of the backing card:

| `size` | Slice of backing GPU | Quota cost |
|--------|----------------------|------------|
| `large` *(default)* | Half | 1x |
| `xlarge` | Full | 2x |

Default `large` gives half a physical GPU, so memory bandwidth and compute are significantly lower than the full card's specs. Use `xlarge` only when the workload genuinely needs the extra memory or compute.

> **Backing PU changes wte in a generator and expects another handler to see those mutations will silently use stale data.
- **Every yield including a `gr.State` value triggers a full pickle round-trip.** For large state (model sessions, frame buffers), minimize how often you yield it — ideally once at the end. Use `gr.update()` for the state slot on intermediate yields.
- **CUDA tensors inside state must be moved to CPU before yielding** — same `torch.cuda._lazy_init()` issue as above.

## Concurrency

Handlers run **concurrently by default** on ZeroGPU. This is not opt-in. Code that worked in single-user testing can silently corrupt or leak data in production.

Three rules. Full treatment with examples in `references/concurrency.md`.

1. **No mutable global state.** Concurrent requests overwrite each other.
2. **No fixed file paths for outputs.** Concurrent requests clobber the same file. Use `tempfile` for unique paths.
3. **Read-only globals are safe.** Model objects, tokenizers, configs loaded once at startup and only read during requests are safe and encouraged.

## Call Granularity

Each entry into a `@spaces.GPU` function carries non-trivial cost — pickle round-trip across the process boundary, worker warm-up, CUDA re-attach, and a fresh pass through the node-level queue. Calling a decorated function from inside a hot loop multiplies these costs and adds a new failure mode: a later iteration may fail to acquire a GPU slot, stalling the whole job mid-way.

Decorate the outer function that owns the loop, not the per-iteration worker:

```python
# Avoid — N GPU entries for N frames
def process_video(frames):
    return [process_frame(f) for f in frames]

@spaces.GPU(duration=...)
def process_frame(frame):
    ...

# Prefer — one GPU entry for the whole video
@spaces.GPU(duration=...)
def process_video(frames):
    return [process_frame(f) for f in frames]

def process_frame(frame):
    ...
```

If the loop mixes heavy CPU work with GPU work, wrapping the whole loop charges that CPU time against the user's quota. When that cost is material, batching the GPU work so CPU pre/post-processing stays outside the decorator is a situational optimization — not the default.

## CUDA Build Constraints

HF Spaces builds Docker images in a CPU-only environment. **On ZeroGPU, the build phase has no `nvcc`** because the base image is `python:3.13` (dedicated-GPU Spaces use `nvidia/cuda:*-devel-*` and have `nvcc` at build time). A CUDA-dependent package whose only distribution is sdist — e.g. bare `flash-attn` — therefore cannot be installed via `requirements.txt` on ZeroGPU. Only pre-built wheels work.

ZeroGPU **runtime** does have `nvcc` available, mounted from a CUDA devel image at `/cuda-image` since 2025-07 (originally added for AoTI support). This is what makes `torch.export` / AoTI workflows possible inside `@spaces.GPU` calls.

**Bottom line**: install every CUDA-dependent package from a pre-built wheel. If no wheel is available on PyPI, build one externally (e.g. host on HF Hub) and pin the URL. For `flash-attn`, the upstream releases page ships a fairly complete wheel matrix covering most Python × CUDA × torch combinations.

For wheel-tag reading (cxx11 ABI, `cu12torch2.X`, `cp3XX`), torch-family side-car drift, and the kernels-community fallback, see `references/cuda-and-deps.md`.

## Example Caching

`gr.Examples` behavior is environment-dependent. On ZeroGPU specifically:

- `cache_examples` defaults to `True` (Spaces sets `GRADIO_CACHE_EXAMPLES=true`).
- `cache_mode` defaults to `"lazy"` (Spaces sets `GRADIO_CACHE_MODE=lazy` only on ZeroGPU).

ZeroGPU defaults to `lazy` because eager caching pre-runs every example at app startup, but ZeroGPU has **no GPU attached at startup** — only during request handling. Eager caching of GPU-bound examples would fail there.

When `cache_examples=True`, the `run_on_click` / `run_examples_on_click` parameter is silently ignored. If your app relies on click-populates-only behavior, set `cache_examples=False` explicitly to preserve it.

To reproduce ZeroGPU example-caching behavior locally:

```bash
GRADIO_CACHE_EXAMPLES=true GRADIO_CACHE_MODE=lazy python app.py
```

## Dependency Management

### `python_version` pin in README frontmatter

Pinning `python_version` is **effectively required** for ZeroGPU. The runtime default is currently Python 3.10, so a local environment using 3.11+ will fail to install on the Space without an explicit pin. Pin to a ZeroGPU-supported version (3.12 is a reasonable default); the authoritative supported list lives in the [ZeroGPU docs](https://huggingface.co/docs/hub/spaces-zerogpu) — do not hardcode the full list, refer to the docs.

```yaml
# README.md frontmatter
python_version: "3.12"
```

Both `"3.12"` and `"3.12.12"` forms are accepted.

### Do not pin `spaces` in `requirements.txt`

The Space platform pins its own `spaces` version. A conflicting pin in `requirements.txt` causes pip resolution to fail at build time.

> **Rule**: Do not include `spaces` in `requirements.txt`.

How to achieve this depends on your tooling:

- **Hand-written `requirements.txt`**: simply omit `spaces`.
- **uv** (`pyproject.toml`-managed): declare `spaces` in `pyproject.toml` so uv co-resolves transitive constraints (notably `psutil`, which `spaces` pins), then exclude it from the export:
  ```bash
  uv export --no-hashes --no-dev --no-emit-package spaces -o requirements.txt
  ```
  Without `spaces` in `pyproject.toml`, uv cannot see its transitive constraints and may resolve incompatible versions at build time.
- **pip-tools** (`pip-compile`) / **Poetry**: use the equivalent exclude mechanism.

### Pin `torch` to match wheel tags

If you install a CUDA-dependent wheel via direct URL, the wheel filename encodes the `torch` major.minor it was built against (e.g. `cu12torch2.8`). Pin `torch==X.Y.Z` in `requirements.txt` to match — otherwise pip may resolve `torch` to a different version and the Space fails on first import. Details and the kernels-community alternative are in `references/cuda-and-deps.md`.
