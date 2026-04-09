<img src="https://capsule-render.vercel.app/api?type=waving&color=0:ff69b4,50:bd93f9,100:00fcd6&height=120&section=header" width="100%" alt="" />

<div align="center">

```
█▀▀ ▄▀█ ▀█▀ ▄▀█ █░░ █▄█ █▀ ▀█▀
█▄▄ █▀█ ░█░ █▀█ █▄▄ ░█░ ▄█ ░█░
```

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Orbitron&size=20&duration=3000&pause=1000&color=00fcd6&center=true&vCenter=true&width=600&lines=Infrastructure+engineer.+Data+architect.+Design+system+builder.;From+GPU+pipelines+to+Kubernetes+operators;Building+the+tools+that+build+the+things)](https://github.com/TheBranchDriftCatalyst)

*I build the infrastructure layer between raw data and useful knowledge — from bare-metal Kubernetes clusters to the ML pipelines and UI systems that make data accessible.*

**DJ** · Platform Engineer

[LinkedIn](https://linkedin.com/in/yourprofile)

<br/>

<img src="https://skillicons.dev/icons?i=ansible,bash,cloudflare,django,docker,fastapi,go,grafana,js,kubernetes,nextjs,nix,playwright,postgres,prometheus,py,react,redis,swift,tailwind,terraform,ts,vite,webpack&theme=dark&perline=15" alt="Tech Stack" />

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

### [catalyst-data](https://github.com/TheBranchDriftCatalyst/catalyst-data)  ![ACTIVE](https://img.shields.io/badge/ACTIVE-00fcd6?style=flat-square)

> 38-asset knowledge graph construction platform with MCP-contracted LLM extraction, dual-write KG (PostgreSQL+pgvector + Neo4j), GPU-accelerated transcription, and cross-source entity resolution running on a 5-node Talos cluster

![Argo CD](https://img.shields.io/badge/Argo%20CD-EF7B4D?style=flat-square&logo=argocd&logoColor=white) ![Dagster](https://img.shields.io/badge/Dagster-654FF0?style=flat-square&logo=dagster&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) ![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white) ![Kustomize](https://img.shields.io/badge/Kustomize-326CE5?style=flat-square&logo=kustomize&logoColor=white) ![MinIO](https://img.shields.io/badge/MinIO-C72E49?style=flat-square&logo=minio&logoColor=white) ![Neo4j](https://img.shields.io/badge/Neo4j-008CC1?style=flat-square&logo=neo4j&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white) ![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white) ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)

- 38 Dagster assets across 4 code locations (12 congress, 10 media, 13 open-leaks, 3 knowledge-graph) with Bronze/Silver/Gold/Platinum medallion architecture
- 3-package LLM contract validation system with MCP-enforced structured output, 9 ConfigMap-mounted prompt templates, and 198 tests at 97% coverage
- GPU-accelerated transcription: dual backend (OpenVINO + faster-whisper) with automatic CPU fallback
- Speaker diarization with pyannote + word-level alignment
- LLM-based NER and qualified S-P-O assertion extraction with negation/hedge detection
- Cross-source entity resolution (EDC framework) across 4 domains
- Dual-write knowledge graph: PostgreSQL+pgvector + Neo4j
- 22 Prometheus metrics across 8 subsystems with 32 Kubernetes manifests
- QSV AV1 hardware video transcoding for ultra compression
- 13-page Streamlit data explorer with asset browser, semantic search, knowledge graph viz

---

### [talos-homelab](https://github.com/TheBranchDriftCatalyst/talos-homelab)  ![ACTIVE](https://img.shields.io/badge/ACTIVE-00fcd6?style=flat-square)

> Production Talos Linux Kubernetes cluster with dual GitOps (Flux + ArgoCD), full LGTM observability stack, multi-cluster connectivity via Nebula mesh, and 30+ infrastructure components

- 5-node Talos Linux immutable cluster (1 control plane, 3 workers, 1 GPU node with Intel Arc) plus AWS k3s node for hybrid multi-cluster
- 30 infrastructure components under Flux Kustomization: Cilium CNI with ClusterMesh + Hubble, Traefik ingress, cert-manager, Authentik SSO, External Secrets with 1Password Connect
- Full LGTM observability stack: Mimir, Loki, Tempo, Alloy, OTel operator, Grafana Operator with 20+ custom dashboards, plus Graylog/OpenSearch/FluentBit
- Dual GitOps: 30 Flux Kustomizations for infrastructure, ArgoCD with image-updater for application workloads

---

### [gateway-arr](https://github.com/TheBranchDriftCatalyst/gateway-arr)  ![WIP](https://img.shields.io/badge/WIP-f7ca33?style=flat-square)

> Kubernetes operator that watches Widget CRDs across namespaces, reconciles them into Homepage-compatible ConfigMaps, and serves a Gin REST API with WebSocket push for real-time dashboard updates

- Custom Widget CRD (gateway.catalyst.io/v1alpha1) with kubebuilder markers, status subresource, health tracking, and credential SecretRef injection
- Reconciler watches Widgets cluster-wide, groups by category labels, and writes a merged services.yaml ConfigMap every 30s
- Gin REST API on :8082 with gorilla/websocket push — clients get live widget state without polling
- Credentials stay in-cluster: SecretKeySelector refs resolve into HOMEPAGE_VAR_ env placeholders

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
| **openscad** | Python build system for parametric OpenSCAD models — define variations in YAML, render STLs in parallel via Jinja2-te... | `WIP` |

### Ai Ml

| Project | Description | Status |
|:--------|:------------|:------:|
| **catalyst-llm** | Self-hosted LLM infrastructure stack with unified multi-provider proxy (LiteLLM), multiple chat UIs, web search (Sear... | `ACTIVE` |
| **memeX** | Hybrid discourse extraction pipeline combining spaCy NER, SentenceTransformer embeddings, rule-based proposition extr... | `ACTIVE` |

### Browser Extensions

| Project | Description | Status |
|:--------|:------------|:------:|
| **catalyst-swiss-army-knife** | Chrome MV3 extension with a pluggable applet architecture that intercepts network requests and renders site-specific ... | `WIP` |

### Catalyst Core

| Project | Description | Status |
|:--------|:------------|:------:|
| **[catalyst-images](https://github.com/TheBranchDriftCatalyst/catalyst-images)** | Nix flake as single source of truth for reproducible, layered Docker dev environment images with 8 variants, cross-pl... | `ACTIVE` |
| **catalyst-py** | Python utilities monorepo with an ActiveRecord-pattern Google Calendar ORM, multiprocess Goodreads scraper, Audible b... | `ACTIVE` |
| **cli-tools** | Go CLI tools and shell scripts for developer workflow automation — multi-process TUIs, git branch management, Docker/... | `ACTIVE` |
| **[dotfiles-2024](https://github.com/TheBranchDriftCatalyst/dotfiles-2024)** | Dotbot-based dotfiles management system with fzf-driven profile selection, modular ZSH config, and domain-scoped Brew... | `ACTIVE` |
| **machines** | Ansible infrastructure automation with 12 idempotent roles for machine provisioning, SOPS/GPG secrets, dotfiles deplo... | `ACTIVE` |

### Data Science

| Project | Description | Status |
|:--------|:------------|:------:|
| **[notebooks](https://github.com/TheBranchDriftCatalyst/notebooks)** | 38+ Jupyter notebooks across 9 topic domains with ML backtesting, NLP pipelines, demographics research, and a multi-d... | `ACTIVE` |

### Devops

| Project | Description | Status |
|:--------|:------------|:------:|
| **swarm-graph** | Docker topology explorer — Go agent watches the daemon via event stream and serves a React/D3 frontend with force-dir... | `ACTIVE` |

### Homelab

| Project | Description | Status |
|:--------|:------------|:------:|
| **kasa-exporter** | Prometheus exporter for TP-Link Kasa smart plugs with real-time power monitoring, time-of-use energy cost tracking, a... | `ACTIVE` |

### Infrastructure

| Project | Description | Status |
|:--------|:------------|:------:|
| **catalyst-dns-sync** | Kubernetes-native DNS controller that watches Ingress and Traefik IngressRoute resources and syncs hostnames to Techn... | `WIP` |
| **talos-private** | Kubernetes GitOps manifests for private media services deployed via ArgoCD with Kustomize, extending the talos-homela... | `ACTIVE` |

### Macos Native

| Project | Description | Status |
|:--------|:------------|:------:|
| **catalyst-swift** | Shared SwiftUI component library providing the Catalyst cybersynthpunk dark theme, glass-card effects, neon glow modi... | `ACTIVE` |

### Meta

| Project | Description | Status |
|:--------|:------------|:------:|
| **catalyst-sdlc-framework** | Multi-agent SDLC framework implementing a Cognitive Council deliberation protocol — 6 specialized expert agents colla... | `ACTIVE` |
| **[TheBranchDriftCatalyst](https://github.com/TheBranchDriftCatalyst/TheBranchDriftCatalyst)** | GitHub profile page generator with synthwave styling and AI-powered project summaries | `ACTIVE` |

### Serverless

| Project | Description | Status |
|:--------|:------------|:------:|
| **notion-cloudflare-blog-worker** | Cloudflare Worker that reverse-proxies Notion pages onto a custom domain with clean slug-based URLs, edge-injected da... | `ACTIVE` |

### Web Apps

| Project | Description | Status |
|:--------|:------------|:------:|
| **dungeon-library** | Fantasy fiction reading platform with a dark-dungeon aesthetic — browse, read, review, and track progress across seri... | `ACTIVE` |
| **[hakboard-dashboard](https://github.com/TheBranchDriftCatalyst/hakboard)** | Smart home kiosk dashboard built as a DakBoard replacement, featuring drag-and-drop widget grid layout, radial weathe... | `WIP` |

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
