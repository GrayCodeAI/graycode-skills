---
name: design-system-tokens
description: "Maintain UI component consistency and design tokens, and sync design tool output to code workflows."
license: MIT
tags:
- design-system
- design-tokens
- ui
---

# Design Systems

## Core Principles
- **Consistency**: Reusable components and tokens across the UI.
- **Single Source of Truth**: Design tokens sync Figma and Codebase.

## Figma to Code Workflow
```mermaid
%%{init: {"theme": "default", "flowchart": {"useMaxWidth": true}}}%%
flowchart TD
    A[Figma Design] --> B[Export Design Tokens]
    B --> C[Style Dictionary]
    C --> D[CSS/SCSS Variables]
    D --> E[UI Components]
```

## Template: Design Token
```json
{
  "color": {
    "primary": {
      "value": "#0052cc",
      "type": "color"
    },
    "text": {
      "value": "#172b4d",
      "type": "color"
    }
  }
}
```
