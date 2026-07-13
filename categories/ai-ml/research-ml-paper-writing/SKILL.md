---
name: research-ml-paper-writing
description: Write publication-ready ML/AI papers for NeurIPS, ICML, ICLR, ACL, AAAI,
  COLM. Use when drafting papers from research repos, structuring arguments, verifying
  citations, or preparing camera-ready su...
license: MIT
tags:
- academic-writing
- neurips
- icml
- paper-writing
- research
version: 1.2.0
author: Orchestra Research
dependencies:
- semanticscholar
- arxiv
- habanero
- requests
---

## References & Resources

### Reference Documents (Deep Dives)

| Document | Contents |
|----------|----------|
| writing-guide.md | Gopen & Swan 7 principles, Ethan Perez micro-tips, word choice |
| citation-workflow.md | Citation APIs, Python code, BibTeX management |
| checklists.md | NeurIPS 16-item, ICML, ICLR, ACL requirements |
| reviewer-guidelines.md | Evaluation criteria, scoring, rebuttals |
| sources.md | Complete bibliography of all sources |

### LaTeX Templates

Templates in `templates/` directory:
- **ML/AI**: ICML 2026, ICLR 2026, NeurIPS 2025, ACL/EMNLP, AAAI 2026, COLM 2025
- **Systems** (OSDI, NSDI, ASPLOS, SOSP): See [systems-paper-writing]() skill

**Compiling to PDF:**
- **VS Code/Cursor**: Install LaTeX Workshop extension + TeX Live → Save to auto-compile
- **Command line**: `latexmk -pdf main.tex` or `pdflatex` + `bibtex` workflow
- **Online**: Upload to [Overleaf](https://overleaf.com)

See templates/README.md for detailed setup instructions.

### Key External Sources

**Writing Philosophy:**
- [Neel Nanda: How to Write ML Papers](https://www.alignmentforum.org/posts/eJGptPbbFPZGLpjsp/highly-opinionated-advice-on-how-to-write-ml-papers) - Narrative, "What/Why/So What"
- [Farquhar: How to Write ML Papers](https://sebastianfarquhar.com/on-research/2024/11/04/how_to_write_ml_papers/) - 5-sentence abstract
- [Gopen & Swan: Science of Scientific Writing](https://cseweb.ucsd.edu/~swanson/papers/science-of-writing.pdf) - 7 reader expectation principles
- [Lipton: Heuristics for Scientific Writing](https://www.approximatelycorrect.com/2018/01/29/heuristics-technical-scientific-writing-machine-learning-perspective/) - Word choice
- [Perez: Easy Paper Writing Tips](https://ethanperez.net/easy-paper-writing-tips/) - Micro-level clarity

**APIs:** [Semantic Scholar](https://api.semanticscholar.org/api-docs/) | [CrossRef](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) | [arXiv](https://info.arxiv.org/help/api/basics.html)

**ML/AI Venues:** [NeurIPS](https://neurips.cc/Conferences/2025/PaperInformation/StyleFiles) | [ICML](https://icml.cc/Conferences/2025/AuthorInstructions) | [ICLR](https://iclr.cc/Conferences/2026/AuthorGuide) | [ACL](https://github.com/acl-org/acl-style-files)

**Systems Venues:** See the [systems-paper-writing]() skill for OSDI, NSDI, ASPLOS, SOSP links and guides
