---
name: std-common-architecture-diagramming
description: "Standards for creating clear, audience-appropriate C4 and UML architecture diagrams with Mermaid. Use when producing system context diagrams, container views, sequence diagrams, or updating ARCHITE..."
license: MIT
tags: [general]
metadata: None
triggers: None
files: None
keywords: None
---

# Architecture Diagramming Standard

## **Priority: P1 (Standard)**

## Guidelines

- **Use C4 Model**: Context -> Container -> Component -> Code.
- **Audience-Centric**: Tailor abstraction (Execs vs. Devs).
- **Select Type**: Sequence (Protocol), ERD (Data), State (Lifecycle), Cloud (Infra). See Selection.
- **Explicit Labels**: Label every arrow (e.g., "Uses", "HTTPS").
- **Consistent Notation**: Cylinders=DB, Rectangles=Systems, Dashed=Async.
- **Metadata**: Title, Date, Version, Author.
- **Legend Mandatory**: Define all shapes/colors/styles.
- **Direction**: `graph LR` (Flow) or `graph TD` (Hierarchy).
- **Deployment**: Map containers to infrastructure.
- **Governance**: CRITICAL: Review best-practices.md before starting.

See implementation examples for C4 container diagram in Mermaid.

## Anti-Patterns

- **Mixed Levels**: DB columns in System Context.
- **Unlabeled Arrows**: Ambiguous relations.
- **Mystery Shapes**: Undefined in Legend.
- **Dead Ends**: Unconnected nodes.
- **Clutter**: >20 nodes/diagram.
- **Acronyms**: Undefined abbreviations.

## References

- Diagram Selection
- Cloud Architecture
- C4 Model Guide
- Checklist
- Best Practices