---
name: unclosed-frontmatter-fixture
description: "Invalid fixture with an unclosed frontmatter block for a skill-format-check harness. Load when validating that the checker rejects a skill whose frontmatter is never terminated."
license: MIT
tags:
- testing
- fixture
- skill-format
---

---
name: bad-skill-unclosed
version: 1.0.0
description: "This skill has an unclosed frontmatter block."
metadata: {}

# Unclosed Frontmatter Skill

This frontmatter does not have a closing `---` block.