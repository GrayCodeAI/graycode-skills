---
name: skill-standardization
description: Standardize and validate SKILL.md files to match the project specification.
  Use when creating new skills, converting existing skills to standard format, or
  validating skill file structure. Handles ...
license: MIT
tags:
- skill-management
- standardization
- validation
- automation
- scripting
allowed-tools: Bash Read Write Edit Glob Grep
metadata: None
platforms: Claude, ChatGPT, Gemini
---

# Skill Title

## When to use this skill
- Scenario 1
- Scenario 2

## Instructions

### Step 1: [Action]
Content...

### Step 2: [Action]
Content...

## Examples

### Example 1: [Scenario]
Content...

## Best practices
1. Practice 1
2. Practice 2

## References
- Link
```

## Examples

### Example 1: Convert a single file manually

```python
from pathlib import Path
import re

filepath = Path('backend/new-skill/SKILL.md')
content = filepath.read_text()

# Normalize legacy headings to standard
content = content.replace('## Best Practices', '## Best practices')
content = content.replace('## Reference', '## References')
content = re.sub(r'### Step (\d+):', r'### Step \1:', content)

filepath.write_text(content)
```

### Example 2: Validate a skill file

```bash
# Check for required sections
grep -E "^## (When to use|Instructions|Examples|Best practices|References)" SKILL.md
```

## Best practices

1. **Run all three scripts in sequence** for complete standardization
2. **Review changes** before committing to ensure content wasn't lost
3. **Keep section content** - only headings are converted, not content
4. **Test with one file first** when making script modifications

## References

- README.md - Repository overview and SKILL.md conventions
- .agent-skills/README.md - Skill repository structure and examples
