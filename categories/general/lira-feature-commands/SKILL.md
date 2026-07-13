---
name: lira-feature-commands
description: 'Skill: lira-feature-commands'
license: MIT
tags:
- general
---

Your goal is to learn the requirements of a GitHub issue...
```

## CLI Usage

### Interactive Mode

```bash
npx agent-rules
```

The CLI will prompt:
1. Which AI App?
2. Which topics?
3. Include MCP configuration?
4. Include custom commands? ← New prompt

### Command Line Flags

```bash
# Include commands with GitHub Copilot
npx agent-rules --app github-copilot --topics secure-code --commands

# Short flag
npx agent-rules -a github-copilot -t testing -c

# Combine with MCP
npx agent-rules --app github-copilot --topics testing --mcp --commands
```

## Behavior by Adapter

| Adapter | Commands Support | Target Directory | File Transform |
|---------|-----------------|------------------|----------------|
| GitHub Copilot | ✅ | `.github/prompts/` | `.command.md` → `.prompt.md` |
| Cursor | ❌ (future) | N/A | N/A |
| Gemini | ❌ (future) | N/A | N/A |
| Claude Code | ❌ (future) | N/A | N/A |

## Error Handling

The feature handles several error scenarios gracefully:

1. **Missing `_commands/` directory**: Silently skipped (returns null)
2. **Unsupported adapter**: Commands not processed if `getCommandsConfig()` returns null
3. **File read/write errors**: Warnings logged, processing continues
4. **Invalid permissions**: Warnings logged, file skipped

## Testing

The feature includes:

1. **Unit tests**: Verify adapter configurations and file transformations
2. **Integration tests**: End-to-end scaffolding with commands enabled/disabled
3. **CLI tests**: Command line flags and interactive prompts

## Future Enhancements

Potential future improvements:

1. **Additional Adapter Support**: Implement commands for Cursor, Gemini, and Claude Code
2. **Custom Transformations**: Allow per-command content transformations
3. **Command Categories**: Support subdirectories within `_commands/`
4. **Command Validation**: Validate frontmatter format and required fields
5. **Command Updates**: Smart merging of existing vs new commands

## Migration Guide

For existing users, this is a non-breaking change:

- Commands are **optional** and disabled by default
- No changes to existing instruction or MCP scaffolding
- New `--commands` flag must be explicitly provided

## Related Documentation

- MCP Feature Documentation - Similar scaffolding pattern
- Adapter Development - How to extend adapters
- Design Overview - Overall architecture
