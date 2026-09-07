---
name: note-taking-management
description: "Creates and updates structured notes for projects, challenges, achievements, transcriptions, and job applications, preserving meeting and lecture notes."
license: MIT
tags:
- note-taking
- documentation
- knowledge-management
- meeting-notes
---

# Notes

Creates and manages Obsidian notes using the Obsidian MCP for structured documentation.

## Triggers

- **Project note** ("create project", "new project note", "document project") → project.md
- **Challenge note** ("technical challenge", "take-home", "coding interview", "system design") → challenge.md
- **Brag entry** ("brag document", "achievement", "accomplishment") → brag.md
- **Transcription** ("transcription", "meeting notes", "1:1 notes", "feedback notes", "standup notes", "lecture notes", "course notes") → transcription.md
- **Company tracking** ("company note", "track interview", "job application") → company.md

## Workflow

```text
resolve-vault → select-type → compose-note → write → link-related
```

Each note type has its own workflow. Use any type independently.
