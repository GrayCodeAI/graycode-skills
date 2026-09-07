---
name: whiteboard-editing
description: "View and edit whiteboards through a suite CLI: export previews, extract structure, and update content from diagrams. Use when a user wants to read or modify a whiteboard."
license: MIT
tags:
- whiteboard
- diagram
- editing
---

> [!IMPORTANT]
> - 运行 `lark-cli --version`，确认可用，无需询问用户。
> - 运行 `npx -y @larksuite/whiteboard-cli@^0.2.13 -v`，确认可用，无需询问用户。

**CRITICAL — 开始前 MUST 先用 Read 工具读取 `lark-shared/SKILL.md`，其中包含认证、权限处理**

---

## 快速决策

**身份**：画板操作默认使用 `--as user`。仅当需要以应用身份上传时使用 `--as bot`。

> 先判断「只读还是写入」，再在对应表内按上到下匹配，**命中即停**。

### A. 只读 · 查看 / 导出（不改画板）

| 用户需求 | 行动 |
|---|---|
| 查看画板内容 / 导出图片 | `+export --output-type preview`                       |
| 导出 SVG 矢量图 | `+export --output-type svg`                       |
| 提取画板的 Mermaid/PlantUML 源码 | `+export --output-type source` |

### B. 写入 · 创作 / 编辑（会改画板，命中即停）

| 场景 | 行动 | 写入方式 | 对原内容 |
|---|---|---|---|
| 用户**已提供** Mermaid/PlantUML/SVG 代码，或明确指定用该格式 | 使用该代码 → `+update`，`--input_format` 取单值 `mermaid` / `plantuml` / `svg`；写入非空已有画板并需要 overwrite 时，先确认会整板重建；若 SVG 用于修改已有画板，先走 `routes/svg-edit.md` 有损确认 | overwrite / append | 按用户要求 |
| 从零新建复杂图表（架构/流程/组织等） | → **§ 创作 Workflow** | 首次写入 | — |
| 修改 / 增补已有画板 | → **§ 编辑 Workflow** | 见该表 | 见该表 |

## Shortcuts

| Shortcut                                          | 说明 |
|---------------------------------------------------|---|
| `+export` | 导出画板为预览图片、SVG 矢量图、代码或原始节点结构。 |
| `+update` | 更新画板，支持 PlantUML、Mermaid、SVG 或 OpenAPI 原生格式 |

---

## 不在本 skill 范围
- 文档内容编辑 → lark-doc lark-doc
- 在文档中创建画板 → lark-doc-whiteboard.md
- 表格 / Base 操作 → lark-sheets / lark-base
