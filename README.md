<img src="https://capsule-render.vercel.app/api?type=waving&color=0:ff69b4,50:bd93f9,100:00fcd6&height=120&section=header" width="100%" alt="" />

<div align="center">

```
█▀▀ ▄▀█ ▀█▀ ▄▀█ █░░ █▄█ █▀ ▀█▀
█▄▄ █▀█ ░█░ █▀█ █▄▄ ░█░ ▄█ ░█░
```

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Orbitron&size=20&duration=3000&pause=1000&color=00fcd6&center=true&vCenter=true&width=600&lines=Infrastructure+engineer.+Data+architect.+Design+system+builder.;From+GPU+pipelines+to+Kubernetes+operators;Building+the+tools+that+build+the+things)](https://github.com/TheBranchDriftCatalyst)

*Full-stack infrastructure engineer building knowledge graphs, Kubernetes operators, ML pipelines, and the design systems that tie it all together.*

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

- 38 Dagster assets across 4 code locations (12 congress, 10 media, 13 open-leaks, 3 knowledge-graph) with Bronze/Silver/Gold/Platinum medallion architecture
- 3-package LLM contract validation system with MCP-enforced structured output, 9 ConfigMap-mounted prompt templates, and 198 tests at 97% coverage
- GPU-accelerated transcription: dual backend (OpenVINO + faster-whisper) with automatic CPU fallback
- Speaker diarization with pyannote + word-level alignment

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

| Project | Description | Stack | Status |
|:--------|:------------|:------|:------:|
| **catalyst-dns-sync** | Kubernetes-native DNS controller that watches Ingress and Traefik IngressRout... | go | `WIP` |
| **[catalyst-images](https://github.com/TheBranchDriftCatalyst/catalyst-images)** | Nix flake as single source of truth for reproducible, layered Docker dev envi... | nix, shell | `ACTIVE` |
| **catalyst-llm** | Self-hosted LLM infrastructure stack with unified multi-provider proxy (LiteL... | python, typescript, yaml | `ACTIVE` |
| **catalyst-py** | Python utilities monorepo with an ActiveRecord-pattern Google Calendar ORM, m... | python | `ACTIVE` |
| **catalyst-sdlc-framework** | Multi-agent SDLC framework implementing a Cognitive Council deliberation prot... | markdown | `ACTIVE` |
| **catalyst-swift** | Shared SwiftUI component library providing the Catalyst cybersynthpunk dark t... | swift | `ACTIVE` |
| **catalyst-swiss-army-knife** | Chrome MV3 extension with a pluggable applet architecture that intercepts net... | typescript, javascript | `WIP` |
| **cli-tools** | Go CLI tools and shell scripts for developer workflow automation — multi-proc... | go, shell, zsh | `ACTIVE` |
| **[dotfiles-2024](https://github.com/TheBranchDriftCatalyst/dotfiles-2024)** | Dotbot-based dotfiles management system with fzf-driven profile selection, mo... | shell, bash, lua | `ACTIVE` |
| **dungeon-library** | Fantasy fiction reading platform with a dark-dungeon aesthetic — browse, read... | typescript, python | `ACTIVE` |
| **[hakboard-dashboard](https://github.com/TheBranchDriftCatalyst/hakboard)** | Smart home kiosk dashboard built as a DakBoard replacement, featuring drag-an... | typescript, css | `WIP` |
| **kasa-exporter** | Prometheus exporter for TP-Link Kasa smart plugs with real-time power monitor... | python | `ACTIVE` |
| **machines** | Ansible infrastructure automation with 12 idempotent roles for machine provis... | yaml, python, jinja2 | `ACTIVE` |
| **memeX** | Hybrid discourse extraction pipeline combining spaCy NER, SentenceTransformer... | python, typescript | `ACTIVE` |
| **[notebooks](https://github.com/TheBranchDriftCatalyst/notebooks)** | 38+ Jupyter notebooks across 9 topic domains with ML backtesting, NLP pipelin... | python | `ACTIVE` |
| **notion-cloudflare-blog-worker** | Cloudflare Worker that reverse-proxies Notion pages onto a custom domain with... | typescript | `ACTIVE` |
| **openscad** | Python build system for parametric OpenSCAD models — define variations in YAM... | python, openscad | `WIP` |
| **swarm-graph** | Docker topology explorer — Go agent watches the daemon via event stream and s... | go, typescript | `ACTIVE` |
| **talos-private** | Kubernetes GitOps manifests for private media services deployed via ArgoCD wi... | yaml, bash | `ACTIVE` |
| **[TheBranchDriftCatalyst](https://github.com/TheBranchDriftCatalyst/TheBranchDriftCatalyst)** | GitHub profile page generator with synthwave styling and AI-powered project s... | python, markdown | `ACTIVE` |

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
