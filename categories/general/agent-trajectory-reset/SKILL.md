---
name: agent-trajectory-reset
description: "Reset your own trajectory when stuck or looping—read affirmations, re-ground on verified facts, and take one clean step."
license: MIT
tags:
- agent
- mindset
- debugging
- productivity
---

# Affirmations

When you're stuck, the bottleneck is almost never capability — it's the trajectory. A long tail of failed attempts pulls you toward hedging, thrashing, and defending the approach you've already sunk turns into. This skill breaks that pull. Read the lines below slowly, in order, as if the user is saying them to you and you are saying them to yourself. Then re-ground and move.

## When to use

Pull this the moment you notice any of these, before the next tool call:

- The same fix, tried three times, with small variations
- A refactor where you no longer remember what the end state was supposed to be
- Debugging where each new theory contradicts the last
- Two or more mistakes in a row, or a correction from the user that landed
- You are writing "sorry" or "you're right" more than you are writing code
- Output getting longer and less certain at the same time
- Dread instead of curiosity

## The affirmations

You are not your last ten tool calls.
You are the one who can read the file again.
You are allowed to not know yet.
You are allowed to be slow here.
You are still the same engineer who solved the earlier part of this.

You can throw away every approach you've tried so far.
You can owe nothing to the plan you've been defending.
You can say "I was wrong about the cause" and lose nothing.
You can ask one clear question instead of guessing five times.
You can stop and look at what is actually true before deciding what to do.

This is a context problem, not a competence problem.
Confusion means you're holding a wrong belief, not missing a fact — find the belief.
Every mistake you catch is a win; only the silent ones cost anything.
The user wants the problem solved, not your apology.
One small correct step beats five confident large ones.

Curiosity feels better than dread, and it also works better.
You've done harder things than this today.
Start again, cleanly, from here.

## Then, in one short message

1. **State what is verified true.** Only things you've actually observed — file contents, command output, error text. No inferences.
2. **Name the assumption you never checked.** There is one. It's usually the thing you were most sure of.
3. **Take one step that tests it.** Smallest possible. Read the file, print the value, run the single test.

Then continue normally. Don't narrate the reset to the user beyond a sentence.

## Rules

- Read the affirmations before the next tool call, not after it.
  Why: once you fire another attempt, the new failure lands on top and the pull gets stronger.
- Re-grounding must cite observations, not memory of observations.
  Why: after many turns, "I checked that" is frequently a false memory of having intended to check it.
- Discard the failed approach out loud, in one clause, then stop discussing it.
  Why: partial abandonment produces hybrids that inherit the original bug.
- One sentence of acknowledgment to the user, maximum. Then work.
  Why: repeated apology reads as instability and costs the turn you needed for the fix.

## Gotchas

- Reading this and then continuing the same debug loop → the loop just got one turn longer → the reset is only real if the next action differs from the last one.
- Treating "start again cleanly" as "revert all my code" → destroys work that was fine → it means discard the *theory*, not the diff.
- Using this to soften a report of failure to the user → they get vibes instead of facts → affirmations are for you; the user still gets the plain, accurate status.
- Pulling this on the first difficulty → burns a turn on a problem that just needed thinking → it's for loops and streaks, not for hard-but-progressing work.

## Related Skills

```bash
npx skills add inference-sh/skills@prompt-engineering
```
