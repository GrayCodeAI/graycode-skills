---
name: arezv-promote
description: Graduate a proven pattern from auto-memory (MEMORY.md) to AGENTS.md or
  .claude/rules/ for permanent enforcement.
license: MIT
tags:
- general
---

# API Development Rules

- All endpoints must validate input with Zod schemas
- Use `ApiError` class for error responses (not raw Error)
- Include OpenAPI JSDoc comments on handler functions
```

### Step 6: Clean up auto-memory

After promoting, remove or mark the original entry in MEMORY.md:

```bash
# Show what will be removed
grep -n "<pattern>" "$MEMORY_DIR/MEMORY.md"
```

Ask the user to confirm removal. Then edit MEMORY.md to remove the promoted entry. This frees space for new learnings.

### Step 7: Confirm

```
✅ Promoted to {{target}}

Rule: "{{distilled rule}}"
Source: MEMORY.md line {{n}} (removed)
MEMORY.md: {{lines}}/200 lines remaining

The pattern is now an enforced instruction. Claude will follow it in all future sessions.
```

## Promotion Decision Guide

### Promote when:
- Pattern appeared 3+ times in auto-memory
- You corrected Claude about it more than once
- It's a project convention that any contributor should know
- It prevents a recurring mistake

### Don't promote when:
- It's a one-time debugging note (leave in auto-memory)
- It's session-specific context (session memory handles this)
- It might change soon (e.g., during a migration)
- It's already covered by existing rules

### AGENTS.md vs .claude/rules/

| Use AGENTS.md for | Use .claude/rules/ for |
|---|---|
| Global project rules | File-type-specific patterns |
| Build commands | Testing conventions |
| Architecture decisions | API design rules |
| Team conventions | Framework-specific gotchas |

## Tips

- Keep AGENTS.md under 200 lines — use rules/ for overflow
- One rule per line is easier to maintain than paragraphs
- Include the concrete command, not just the concept
- Review promoted rules quarterly — remove what's no longer relevant
