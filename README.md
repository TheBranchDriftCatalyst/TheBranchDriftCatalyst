<img src="https://capsule-render.vercel.app/api?type=waving&color=0:ff69b4,50:bd93f9,100:00fcd6&height=120&section=header" width="100%" alt="" />

<div align="center">

```
█▀▀ ▄▀█ ▀█▀ ▄▀█ █░░ █▄█ █▀ ▀█▀
█▄▄ █▀█ ░█░ █▀█ █▄▄ ░█░ ▄█ ░█░
```

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Orbitron&size=20&duration=3000&pause=1000&color=00fcd6&center=true&vCenter=true&width=600&lines=Infrastructure+engineer.+Data+architect.+Design+system+builder.;From+GPU+pipelines+to+Kubernetes+operators;Building+the+tools+that+build+the+things)](https://github.com/TheBranchDriftCatalyst)

*I build the infrastructure layer between raw data and useful knowledge — from bare-metal Kubernetes clusters to the ML pipelines and UI systems that make data accessible.*

**DJ** · Platform Engineer

[LinkedIn](https://www.linkedin.com/in/hdaniels90/)

<br/>

<img src="https://skillicons.dev/icons?i=ansible,bash,cloudflare,docker,fastapi,go,grafana,js,kubernetes,nextjs,nix,playwright,postgres,prometheus,py,react,swift,tailwind,terraform,ts,vite,webpack&theme=dark&perline=15" alt="Tech Stack" />

</div>

---

<div align="center">

<table role="presentation"><tr>
<td><img src="https://streak-stats.demolab.com?user=TheBranchDriftCatalyst&theme=synthwave&hide_border=true&background=0d1117&ring=00fcd6&fire=ff69b4&currStreakLabel=00fcd6&sideLabels=bd93f9" alt="GitHub contribution streak stats" /></td>
<td><img src="https://github-readme-stats-sigma-five.vercel.app/api/top-langs/?username=TheBranchDriftCatalyst&layout=compact&theme=synthwave&hide_border=true&bg_color=0d1117&title_color=00fcd6&text_color=ffffff&icon_color=bd93f9" alt="Most used programming languages" /></td>
</tr></table>

<img src="https://github-readme-activity-graph.vercel.app/graph?username=TheBranchDriftCatalyst&theme=react-dark&hide_border=true&bg_color=0d1117&color=00fcd6&line=ff69b4&point=bd93f9&area=true&area_color=ff69b4" width="95%" alt="Contribution activity graph" />

</div>

---

## Featured Projects

### [catalyst-operator](https://github.com/TheBranchDriftCatalyst/catalyst-operator)  ![WIP](https://img.shields.io/badge/WIP-f7ca33?style=flat-square)

> Operator-IDE for the catalyst-llm stack — single Python FastAPI server (folds bd issues + workspace files + per-repo CI/PR rollup + LangGraph agent) and a React SPA built on @catalyst/llm-sdk PageShell. Replaces the Go dashboard + Express beads-server + sdlc-agent split with one process. Renders mac-sdlc-node's inference machine as a /machine route.

![beads](https://img.shields.io/badge/beads-8B5CF6?style=flat-square&logo=beads&logoColor=white) ![CodeMirror](https://img.shields.io/badge/CodeMirror-D30707?style=flat-square&logo=codemirror&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) ![GitHub CLI](https://img.shields.io/badge/GitHub%20CLI-181717?style=flat-square&logo=gh&logoColor=white) ![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=flat-square&logo=langgraph&logoColor=white) ![LiteLLM](https://img.shields.io/badge/LiteLLM-1A1A1A?style=flat-square&logo=litellm&logoColor=white) ![OpenAPI Codegen](https://img.shields.io/badge/OpenAPI%20Codegen-6BA539?style=flat-square&logo=openapi-typescript-codegen&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black) ![React Router](https://img.shields.io/badge/React%20Router-CA4245?style=flat-square&logo=react-router&logoColor=white) ![Tailwind](https://img.shields.io/badge/Tailwind-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white) ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white) ![uv](https://img.shields.io/badge/uv-DE5FE9?style=flat-square&logo=uv&logoColor=white) ![Uvicorn](https://img.shields.io/badge/Uvicorn-499848?style=flat-square&logo=uvicorn&logoColor=white) ![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat-square&logo=vite&logoColor=white) ![watchfiles](https://img.shields.io/badge/watchfiles-3776AB?style=flat-square&logo=watchfiles&logoColor=white) ![Yarn](https://img.shields.io/badge/Yarn-2C8EBB?style=flat-square&logo=yarn&logoColor=white)

- Single Python FastAPI process replaces three (Go dashboard, Express beads-server, Python sdlc-agent) — agent tools and HTTP routes share services directly with zero HTTP boundary
- Operator-as-MCP-host: spawns MCP servers as stdio subprocesses, exposes their tools BOTH to the LangGraph agent AND directly to the UI as buttons/forms
- UI sets LangGraph state config at runtime via @catalyst/llm-sdk/components/engine/AgentConfigForm — no restart to flip model / temperature / tool subset / max iterations
- Single React SPA replaces beads-ui + workspace-viewer + dashboard chrome; internal routing with lazy chunks per route; PageShell IDE primitive across all surfaces
- Per-repo dashboard rollup: every catalyst_repo.yaml-discovered project gets BD counts + GitHub Actions status + open PRs + commits, rolled up to one cockpit at /
- OpenAPI-generated TS client from FastAPI's /openapi.json — single contract source, zero type drift across the wire

---

### [boomtime](git@github.com:TheBranchDriftCatalyst/hakatime.git)  ![ACTIVE](https://img.shields.io/badge/ACTIVE-00fcd6?style=flat-square)

> A time-tracking application for tracking work hours and generating reports.

---

### [talos-homelab](https://github.com/TheBranchDriftCatalyst/talos-homelab)  ![ACTIVE](https://img.shields.io/badge/ACTIVE-00fcd6?style=flat-square)

> Production Talos Linux Kubernetes cluster with dual GitOps (Flux + ArgoCD), full LGTM observability stack, multi-cluster connectivity via Nebula mesh, and 30+ infrastructure components

- 5-node Talos Linux immutable cluster (1 control plane, 3 workers, 1 GPU node with Intel Arc) plus AWS k3s node for hybrid multi-cluster
- 30 infrastructure components under Flux Kustomization: Cilium CNI with ClusterMesh + Hubble, Traefik ingress, cert-manager, Authentik SSO, External Secrets with 1Password Connect
- Full LGTM observability stack: Mimir, Loki, Tempo, Alloy, OTel operator, Grafana Operator with 20+ custom dashboards, plus Graylog/OpenSearch/FluentBit
- Dual GitOps: 30 Flux Kustomizations for infrastructure, ArgoCD with image-updater for application workloads

---

### [catalyst-data](https://github.com/TheBranchDriftCatalyst/catalyst-data)  ![ACTIVE](https://img.shields.io/badge/ACTIVE-00fcd6?style=flat-square)

> 38-asset knowledge graph construction platform with MCP-contracted LLM extraction, dual-write KG (PostgreSQL+pgvector + Neo4j), GPU-accelerated transcription, and cross-source entity resolution running on a 5-node Talos cluster

- 38 Dagster assets across 4 code locations (12 congress, 10 media, 13 open-leaks, 3 knowledge-graph) with Bronze/Silver/Gold/Platinum medallion architecture
- 3-package LLM contract validation system with MCP-enforced structured output, 9 ConfigMap-mounted prompt templates, and 198 tests at 97% coverage
- GPU-accelerated transcription: dual backend (OpenVINO + faster-whisper) with automatic CPU fallback
- Speaker diarization with pyannote + word-level alignment

---

### [catalyst-ui](https://github.com/TheBranchDriftCatalyst/catalyst-ui)  ![ACTIVE](https://img.shields.io/badge/ACTIVE-00fcd6?style=flat-square)

> Cyberpunk-themed React component library shipping 50+ components, 8 synthwave themes, a D3.js ForceGraph engine with 4 layout algorithms, and a full observability stack — all tree-shakeable ESM exports

- 50+ components across 33 Radix UI primitives, 14 advanced components (ForceGraph, CodeBlock, Timeline, ThreeJS), and specialty cards including a print-ready RPG character sheet resume
- 8 synthwave CSS themes (Catalyst, Dracula, Dungeon, Gold, Laracon, Nature, Netflix, Nord) with 6 cyberpunk effect layers: glow, scanlines, border lasers, gradients, keyframe animations, and debug overlays
- D3.js ForceGraph engine with 4 layout algorithms (force-directed, Dagre, ELK hierarchical, community detection), orthogonal edge routing, and localStorage position persistence
- 133 tests at 99% coverage with Vitest + Testing Library, enforced via CI alongside automated Storybook deployment to GitHub Pages

---

### [pr-widget](https://github.com/TheBranchDriftCatalyst/pr-widget)  ![ACTIVE](https://img.shields.io/badge/ACTIVE-00fcd6?style=flat-square)

> Native macOS menu bar app for GitHub PR management — floating NSPanel dashboard with urgency scoring, inline diff viewer, quick review actions, and AI-powered PR synopses

- LSUIElement menu bar app with NSPanel floating window (statusBar level, canJoinAllSpaces) anchored below status item with neon glow pulse via Core Animation
- Carbon Events API global hotkey (Cmd+Shift+Option+P) registers system-wide via RegisterEventHotKey with user-customizable key combos
- GitHub GraphQL v4 client with ETag-based conditional requests, SHA256 cache keys, LRU eviction, and exponential backoff with Retry-After
- macOS Keychain Services integration storing GitHub PATs per-account with kSecAttrAccessibleWhenUnlockedThisDeviceOnly

---

<details>
<summary><h2>All Projects</h2></summary>

### 3D Design

| Project | Description | Status |
|:--------|:------------|:------:|
| **openscad** | Python build system for parametric OpenSCAD models — define variations in YAML, render STLs in parallel via Jinja2-templated output names and Pydantic-validated parameter schemas | `WIP` |

### Ai Apps

| Project | Description | Status |
|:--------|:------------|:------:|
| **[image-sorter](https://github.com/TheBranchDriftCatalyst/image-sorter)** | Local-vision image categorizer with LangGraph HITL, Gradio chat UI, and a stdio MCP file-mover | `WIP` |

### Ai Ml

| Project | Description | Status |
|:--------|:------------|:------:|
| **catalyst-llm** | Self-hosted LLM infrastructure stack with unified multi-provider proxy (LiteLLM), multiple chat UIs, web search (SearXNG), and a multi-agent orchestration framework (OpenClaw) | `ACTIVE` |

### Browser Extensions

| Project | Description | Status |
|:--------|:------------|:------:|
| **catalyst-swiss-army-knife** | Chrome MV3 extension with a pluggable applet architecture that intercepts network requests and renders site-specific UIs in the popup | `WIP` |

### Catalyst Core

| Project | Description | Status |
|:--------|:------------|:------:|
| **[catalyst-images](https://github.com/TheBranchDriftCatalyst/catalyst-images)** | Nix flake as single source of truth for reproducible, layered Docker dev environment images with 8 variants, cross-platform builds, and Tilt orchestration | `ACTIVE` |
| **cli-tools** | Go CLI tools and shell scripts for developer workflow automation — multi-process TUIs, git branch management, Docker/Kubernetes shell injection, workspace sync, and system diagnostics | `ACTIVE` |
| **[dotfiles-2024](https://github.com/TheBranchDriftCatalyst/dotfiles-2024)** | Dotbot-based dotfiles management system with fzf-driven profile selection, modular ZSH config, and domain-scoped Brewfile packages | `ACTIVE` |
| **machines** | Ansible infrastructure automation with 12 idempotent roles for machine provisioning, SOPS/GPG secrets, dotfiles deployment, and homelab node configuration | `ACTIVE` |

### Data Science

| Project | Description | Status |
|:--------|:------------|:------:|
| **[notebooks](https://github.com/TheBranchDriftCatalyst/notebooks)** | 38+ Jupyter notebooks across 9 topic domains with ML backtesting, NLP pipelines, demographics research, and a multi-domain Streamlit dashboard | `ACTIVE` |

### E2E Swarm Target

| Project | Description | Status |
|:--------|:------------|:------:|
| **[hot-ones](https://github.com/TheBranchDriftCatalyst/hot-ones)** | quiz app used as e2e swarm target | `ACTIVE` |

### Homelab

| Project | Description | Status |
|:--------|:------------|:------:|
| **kasa-exporter** | Prometheus exporter for TP-Link Kasa smart plugs with real-time power monitoring, time-of-use energy cost tracking, and pre-built Grafana dashboards | `ACTIVE` |

### Mac Os

| Project | Description | Status |
|:--------|:------------|:------:|
| **[mac-sdlc-node](https://github.com/TheBranchDriftCatalyst/mac-sdlc-node)** | Mac inference node — Ollama + vLLM-MLX + Whisper + OpenWebUI + ComfyUI launchd services + LiteLLM/model-pull config generation. Operator surface lives at workspace/catalyst-operator/. | `ACTIVE` |

### Macos Native

| Project | Description | Status |
|:--------|:------------|:------:|
| **catalyst-swift** | Shared SwiftUI component library providing the Catalyst cybersynthpunk dark theme, glass-card effects, neon glow modifiers, changelog parser/viewer, and help-tip system for macOS apps | `ACTIVE` |

### Meta

| Project | Description | Status |
|:--------|:------------|:------:|
| **[catalyst-agentic-sdlc](https://github.com/TheBranchDriftCatalyst/catalyst-agentic-sdlc)** | Private Claude Code plugin marketplace hosting the Catalyst family of multi-agent SDLC and workflow plugins — including a 6-expert Cognitive Council that decomposes epics into structured task manifests via a strict 5-phase deliberation protocol | `ACTIVE` |
| **[TheBranchDriftCatalyst](https://github.com/TheBranchDriftCatalyst/TheBranchDriftCatalyst)** | GitHub profile page generator with synthwave styling and AI-powered project summaries | `STABLE` |

### Serverless

| Project | Description | Status |
|:--------|:------------|:------:|
| **notion-cloudflare-blog-worker** | Cloudflare Worker that reverse-proxies Notion pages onto a custom domain with clean slug-based URLs, edge-injected dark mode, Google Fonts, analytics, and SEO meta tags | `ACTIVE` |

### Uncategorized

| Project | Description | Status |
|:--------|:------------|:------:|
| **[factorio-calculator](git@github.com:TheBranchDriftCatalyst/factorio-calculator.git)** |  | `ACTIVE` |
| **[git-repo-template](git@github.com:TheBranchDriftCatalyst/git-repo-template.git)** |  | `ACTIVE` |
| **pentest** |  | `ACTIVE` |

### Web Apps

| Project | Description | Status |
|:--------|:------------|:------:|
| **dungeon-library** | Fantasy fiction reading platform with a dark-dungeon aesthetic — browse, read, review, and track progress across serialized stories, featuring AI-powered content generation via local Ollama LLMs | `ACTIVE` |
| **[hakboard-dashboard](https://github.com/TheBranchDriftCatalyst/hakboard)** | Smart home kiosk dashboard built as a DakBoard replacement, featuring drag-and-drop widget grid layout, radial weather clock, and Notion integration for productivity widgets | `WIP` |

</details>

---

<div align="center">

```
╔══════════════════════════════════════════════════════╗
║  "It works on my machine" — The Catalyst Guarantee  ║
╚══════════════════════════════════════════════════════╝
```

**[TheBranchDriftCatalyst](https://github.com/TheBranchDriftCatalyst)** · *Making git branches drift since 2024*

</div>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00fcd6,50:bd93f9,100:ff69b4&height=100&section=footer" width="100%" alt="" />
