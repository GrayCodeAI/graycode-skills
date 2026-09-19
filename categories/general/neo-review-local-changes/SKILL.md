---
name: neo-review-local-changes
description: 'Skill: neo-review-local-changes'
license: MIT
tags:
- general
---

## Improvements

[Code improvement suggestions from code-quality-reviewer, if any:]

1. **[Description]** - `file:location` - [Reasoning and benefit]
```

##### If you found no issues

```markdown
# Local Changes Review Report

**Quality Gate**: PASS
No issues found above the configured threshold.

**Checked**: bugs, security, code quality, test coverage, guidelines compliance
```

#### JSON Template

When `--json` flag is set, output results in this JSON structure:

```jsonc
{
  "quality_gate": "PASS",       // "PASS" or "FAIL" - FAIL when any critical or high issue exists
  "summary": {
    "total_issues": 0,          // count of issues after both filters applied
    "critical": 0,              // count at impact 81-100
    "high": 0,                  // count at impact 61-80
    "medium": 0,                // count at impact 41-60
    "medium_low": 0,            // count at impact 21-40
    "low": 0                    // count at impact 0-20
  },
  "issues": [
    {
      "severity": "critical",   // severity label derived from impact_score range
      "file": "src/auth/session.ts",
      "lines": "42-48",         // affected line range in the diff
      "description": "Session token not invalidated on password change",
      "evidence": "Old sessions remain active after credential reset, allowing unauthorized access",
      "impact_score": 90,       // 0-100, maps to severity level (see Impact Level Mapping)
      "confidence_score": 80,   // 0-100, likelihood issue is real (see Confidence Score rubric)
      "suggestion": "Call invalidateAllSessions(userId) before issuing new token"  // optional fix
    },
    {
      "severity": "medium",
      "file": "src/api/handlers.ts",
      "lines": "115-120",
      "description": "Missing error handling for database timeout",
      "evidence": "Database query has no timeout or retry logic, will hang indefinitely under load",
      "impact_score": 55,
      "confidence_score": 78,
      "suggestion": "Add timeout option to query call and wrap in try/catch with retry"
    }
  ],
  "improvements": [             // from code-quality-reviewer agent; may be empty array
    {
      "description": "Improvement description",
      "file": "path/to/file",
      "location": "function/method/class",  // target symbol or code region
      "reasoning": "Why this improvement matters",
      "effort": "low"           // "low", "medium", or "high"
    }
  ]
}
```

`quality_gate` is `"FAIL"` if any critical or high severity issue exists, `"PASS"` otherwise. The `suggestion` field in issues is optional and may be omitted.

## Evaluation Guidelines

- **Pre-Commit Opportunity**: This review runs on uncommitted local changes, before code enters version history. Treat this as the last line of defense: catch bugs, security holes, and contract violations now, while they are cheapest to fix. Issues found here never reach teammates or CI.
- **Security First**: Any High or Critical security issue automatically makes code not ready to commit
- **Quantify Everything**: Use numbers, not words like "some", "many", "few"
- **Be Pragmatic**: Focus on real issues and high-impact improvements
- **Skip Trivial Issues** in large changes (>500 lines):
  - Focus on architectural and security issues
  - Ignore minor naming conventions unless AGENTS.md explicitly requires them
  - Prioritize bugs over style
- **Improvements Should Be Actionable**: Each suggestion should include concrete code examples
- **Consider Effort vs Impact**: Prioritize improvements with high impact and reasonable effort
- **Align with Project Standards**: Reference AGENTS.md and project guidelines when suggesting improvements
- **Terminal Readability**: The report is consumed in a terminal/console. Use fixed-width-friendly formatting: short lines, clear section separators (`---`), and concise tables. Avoid deeply nested bullet lists or long prose paragraphs that wrap poorly in narrow terminals.

## Remember

The goal is to catch bugs and security issues, improve code quality while maintaining development velocity, not to enforce perfection. Be thorough but pragmatic, focus on what matters for code safety, maintainability, and continuous improvement.

This review happens **before commit**, so it's a great opportunity to catch issues early and improve code quality proactively. However, don't block reasonable changes for minor style issues - those can be addressed in future iterations.
