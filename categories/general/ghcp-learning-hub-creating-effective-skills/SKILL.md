---
name: ghcp-learning-hub-creating-effective-skills
description: Master the art of writing reusable, shareable skill folders that deliver
  consistent results across your team.
license: MIT
tags:
- general
title: Creating Effective Skills
authors: None
lastUpdated: 2026-05-08
estimatedReadingTime: 9 minutes
relatedArticles: None
prerequisites: None
---

# run-test-suite

Execute the project's test suite:

1. Identify the test command from package.json or build files
2. Run tests in the integrated terminal
3. Parse test output for failures
4. Summarize failed tests with relevant file locations
5. Suggest potential fixes based on error messages

Use scripts/parse-test-output.sh to extract structured failure data.
```

## Common Questions

**Q: How do I invoke a skill?**

A: Skills can be invoked in several ways:
- **Slash command**: Type the skill name anywhere in your message (e.g., `/generate-tests fix the failing tests`). Since v1.0.44, slash commands can appear mid-input — you don't have to start with them.
- **Multiple skills in one message**: You can invoke multiple skills in a single message (e.g., `/generate-tests and then /conventional-commit`). Both skills will be executed in sequence.
- **Agent discovery**: Agents can also discover and invoke skills automatically based on the skill's `description` and the user's intent — no slash command required.

**Q: How are skills different from prompts?**

A: Skills replace the older prompt file (`*.prompt.md`) format. Skills offer agent discovery (prompts were manual-only), bundled assets (prompts were single files), and cross-platform portability via the Agent Skills specification. If you have existing prompts, consider migrating them to skills.

**Q: Can skills include multiple files?**

A: Yes! Skills are folders, not single files. You can bundle reference documents, templates, scripts, and any other resources the AI needs. Keep individual assets under 5 MB.

**Q: How do I share skills with my team?**

A: Store skill folders in your repository's `.github/skills/` directory. They're automatically available to all team members with Copilot access when working in that repository.

**Q: Can I invoke multiple skills in one message?**

A: Yes, since v1.0.44. You can include multiple slash commands in a single message (e.g., `/generate-tests and then /conventional-commit`), and the CLI will execute each skill in sequence. Agents can also discover and chain multiple skills during a conversation based on user intent. Each skill invocation is independent, but agents maintain conversation context across invocations.

**Q: Should skills include code examples?**

A: Yes, for clarity. Show examples of desired output format, patterns to follow, or anti-patterns to avoid. For complex schemas or formats, consider bundling them as reference files rather than inline examples.

## Common Pitfalls to Avoid

- ❌ **Vague description**: "Code helper" doesn't help agents discover the skill
  ✅ **Instead**: Write descriptions with trigger keywords: "Generate comprehensive unit tests covering happy path, edge cases, and error conditions"

- ❌ **Missing bundled resources**: Expecting the AI to know your test patterns or schemas
  ✅ **Instead**: Bundle reference docs and templates in the skill folder

- ❌ **Too many responsibilities**: A skill that generates, tests, documents, and deploys
  ✅ **Instead**: Create focused skills for each concern

- ❌ **Hardcoded paths**: Referencing specific project file paths in skill instructions
  ✅ **Instead**: Write generic instructions that work across projects

- ❌ **No examples**: Abstract requirements without concrete guidance
  ✅ **Instead**: Include "Good Example" and "What to Avoid" sections, or bundle templates

## Next Steps

Now that you understand effective skills, you can:

- **Explore Repository Examples**: Browse the [Skills Directory]() for production skills covering diverse workflows
- **Learn About Agents**: [Building Custom Agents]() — When to upgrade from skills to full agents
- **Understand Instructions**: [Defining Custom Instructions]() — Complement skills with automatic context
- **Decision Framework**: Choosing the Right Customization _(coming soon)_ — When to use skills vs other types

**Suggested Reading Order**:
1. This article (creating effective skills)
2. [Building Custom Agents]() — More sophisticated workflows
3. Choosing the Right Customization _(coming soon)_ — Decision guidance

---
