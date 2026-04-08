#!/usr/bin/env python3
"""
GitHub Profile Page Generator v2.1
Scans workspace repositories and generates a synthwave-style profile README
aligned to the catalyst-ui design system.

Color palette (from catalyst-ui dark mode):
  Primary/Cyan:  #00fcd6
  Pink:          #ff69b4
  Purple:        #bd93f9
  Background:    #0d1117
  Yellow:        #f7ca33
  Green:         #50fa7b
"""

import json
import os
import sys
import tempfile
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import quote as urlquote

import yaml
from pydantic import BaseModel, ConfigDict, Field

# Use tomllib (stdlib 3.11+) with tomli fallback
try:
    import tomllib
except ModuleNotFoundError:
    try:
        import tomli as tomllib  # type: ignore[no-redef]
    except ModuleNotFoundError:
        tomllib = None  # type: ignore[assignment]


# ── Constants ────────────────────────────────────────────────────────────────

MAX_FEATURED_HIGHLIGHTS = 4
MAX_CATALOG_DESC_LEN = 80


# ── Pydantic Models ──────────────────────────────────────────────────────────


class TechStack(BaseModel):
    model_config = ConfigDict(extra="ignore")
    languages: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)


class BadgeConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")
    stars: bool = True
    issues: bool = True
    prs: bool = True
    license: bool = True


class RepoMetadata(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="ignore")
    name: str
    description: str = ""
    repo_url: str = ""
    private: bool = False
    status: str = "unknown"
    tech_stack: TechStack = Field(default_factory=TechStack)
    groups: List[str] = Field(default_factory=lambda: ["uncategorized"])
    badges: BadgeConfig = Field(default_factory=BadgeConfig)
    highlights: List[str] = Field(default_factory=list)
    demo_url: str = ""
    repo_path: Optional[Path] = None


class Config(BaseModel):
    model_config = ConfigDict(extra="ignore")
    scan_paths: List[str]
    github_username: str = "TheBranchDriftCatalyst"
    waka_time: Optional[Dict[str, str]] = None
    category_order: Optional[List[str]] = None
    hidden_repos: Optional[List[str]] = None
    featured_repos: List[str] = Field(default_factory=list)
    taglines: List[str] = Field(default_factory=list)
    bio: str = ""


# ── Generator ────────────────────────────────────────────────────────────────


class ProfileGenerator:
    """Generates GitHub profile README from repository metadata."""

    # catalyst-ui design system palette
    CYAN = "00fcd6"
    PINK = "ff69b4"
    PURPLE = "bd93f9"
    BG = "0d1117"
    YELLOW = "f7ca33"
    GREEN = "50fa7b"
    MAGENTA = "c026d3"

    # Internal tech key → skillicons.dev icon name
    SKILL_ICON_MAP = {
        "python": "py", "typescript": "ts", "javascript": "js",
        "go": "go", "rust": "rust", "c": "c", "swift": "swift",
        "react": "react", "vue": "vue", "svelte": "svelte",
        "next": "nextjs", "vite": "vite", "webpack": "webpack",
        "django": "django", "flask": "flask", "fastapi": "fastapi",
        "express": "express", "nestjs": "nestjs",
        "docker": "docker", "kubernetes": "kubernetes",
        "ansible": "ansible", "terraform": "terraform",
        "postgresql": "postgres", "mongodb": "mongodb",
        "redis": "redis", "mysql": "mysql",
        "elasticsearch": "elasticsearch", "opensearch": "elasticsearch",
        "tailwindcss": "tailwind", "cloudflare": "cloudflare",
        "aws": "aws", "gcp": "gcp", "azure": "azure",
        "nginx": "nginx", "jest": "jest", "playwright": "playwright",
        "graphql": "graphql", "prometheus": "prometheus",
        "grafana": "grafana", "nix": "nix", "linux": "linux",
        "bash": "bash",
    }

    STATUS_CONFIG = {
        "active":       ("ACTIVE",       "00fcd6"),
        "wip":          ("WIP",          "f7ca33"),
        "experimental": ("EXPERIMENTAL", "c026d3"),
        "archived":     ("ARCHIVED",     "666666"),
        "unknown":      ("—",            "555555"),
    }

    # shields.io badge specs for known tech
    SHIELD_MAP = {
        # Languages
        "python":       ("Python",       "3776AB", "white"),
        "javascript":   ("JavaScript",   "F7DF1E", "black"),
        "typescript":   ("TypeScript",   "3178C6", "white"),
        "go":           ("Go",           "00ADD8", "white"),
        "rust":         ("Rust",         "000000", "white"),
        "swift":        ("Swift",        "F05138", "white"),
        "c":            ("C",            "A8B9CC", "black"),
        # Frontend
        "react":        ("React",        "61DAFB", "black"),
        "vue":          ("Vue.js",       "4FC08D", "white"),
        "svelte":       ("Svelte",       "FF3E00", "white"),
        "next":         ("Next.js",      "000000", "white"),
        "vite":         ("Vite",         "646CFF", "white"),
        "webpack":      ("Webpack",      "8DD6F9", "black"),
        "tailwindcss":  ("Tailwind",     "06B6D4", "white"),
        # Backend
        "django":       ("Django",       "092E20", "white"),
        "flask":        ("Flask",        "000000", "white"),
        "fastapi":      ("FastAPI",      "009688", "white"),
        "express":      ("Express",      "000000", "white"),
        "nestjs":       ("NestJS",       "E0234E", "white"),
        # Data
        "postgresql":   ("PostgreSQL",   "4169E1", "white"),
        "mongodb":      ("MongoDB",      "47A248", "white"),
        "redis":        ("Redis",        "DC382D", "white"),
        "mysql":        ("MySQL",        "4479A1", "white"),
        "neo4j":        ("Neo4j",        "008CC1", "white"),
        "dagster":      ("Dagster",      "654FF0", "white"),
        "pandas":       ("Pandas",       "150458", "white"),
        "numpy":        ("NumPy",        "013243", "white"),
        "spacy":        ("spaCy",        "09A3D5", "white"),
        "pydantic":     ("Pydantic",     "E92063", "white"),
        # DevOps
        "docker":       ("Docker",       "2496ED", "white"),
        "kubernetes":   ("Kubernetes",   "326CE5", "white"),
        "ansible":      ("Ansible",      "EE0000", "white"),
        "terraform":    ("Terraform",    "7B42BC", "white"),
        "argocd":       ("Argo CD",      "EF7B4D", "white"),
        "argo":         ("Argo",         "EF7B4D", "white"),
        "flux":         ("Flux",         "5468FF", "white"),
        "fluxcd":       ("Flux CD",      "5468FF", "white"),
        "helm":         ("Helm",         "0F1689", "white"),
        "kustomize":    ("Kustomize",    "326CE5", "white"),
        # Networking
        "cilium":       ("Cilium",       "F8C517", "black"),
        "traefik":      ("Traefik",      "24A1C1", "white"),
        "nginx":        ("NGINX",        "009639", "white"),
        "liqo":         ("Liqo",         "00AEC7", "white"),
        # Observability
        "prometheus":   ("Prometheus",   "E6522C", "white"),
        "grafana":      ("Grafana",      "F46800", "white"),
        "loki":         ("Loki",         "F46800", "white"),
        "opensearch":   ("OpenSearch",   "005EB8", "white"),
        "elasticsearch":("Elasticsearch","005571", "white"),
        # Cloud
        "minio":        ("MinIO",        "C72E49", "white"),
        "cloudflare":   ("Cloudflare",   "F38020", "white"),
        "aws":          ("AWS",          "232F3E", "white"),
        "gcp":          ("GCP",          "4285F4", "white"),
        # Security
        "vault":        ("Vault",        "FFEC6E", "black"),
        "authentik":    ("Authentik",    "FD4B2D", "white"),
        "tailscale":    ("Tailscale",    "000000", "white"),
        # Testing
        "jest":         ("Jest",         "C21325", "white"),
        "pytest":       ("Pytest",       "0A9EDC", "white"),
        "playwright":   ("Playwright",   "2EAD33", "white"),
        # Other
        "poetry":       ("Poetry",       "60A5FA", "white"),
        "nix":          ("Nix",          "5277C3", "white"),
    }

    SKIP_PATTERNS = [
        "@types/", "types/", "loader", "plugin-", "eslint",
        "babel", "tslib",
    ]

    def __init__(self, config: Config, script_dir: Path):
        self.config = config
        self.script_dir = script_dir
        self.repos: List[RepoMetadata] = []
        self._tech_cache: Dict[str, set] = {}
        self._errors: List[str] = []

    # ── Scanning ─────────────────────────────────────────────────────────

    def scan_repositories(self):
        """Scan configured paths for catalyst_repo.yaml files."""
        for scan_path in self.config.scan_paths:
            workspace_path = (self.script_dir / scan_path).resolve()
            if not workspace_path.exists():
                print(f"  Skipping non-existent path: {workspace_path}")
                continue

            print(f"Scanning: {workspace_path}")
            for repo_dir in workspace_path.iterdir():
                if not repo_dir.is_dir() or repo_dir.name.startswith("."):
                    continue
                yaml_path = repo_dir / "catalyst_repo.yaml"
                if not yaml_path.exists():
                    continue
                try:
                    with open(yaml_path, "r") as f:
                        data = yaml.safe_load(f)
                    if not data:
                        continue
                    if self.config.hidden_repos and data.get("name") in self.config.hidden_repos:
                        print(f"  - Skipped (hidden): {data.get('name', repo_dir.name)}")
                        continue
                    if "name" not in data:
                        data["name"] = repo_dir.name
                    data["repo_path"] = repo_dir
                    self.repos.append(RepoMetadata(**data))
                    print(f"  + {data['name']}")
                except yaml.YAMLError as e:
                    msg = f"YAML parse error in {yaml_path}: {e}"
                    self._errors.append(msg)
                    print(f"  ! {msg}", file=sys.stderr)
                except Exception as e:
                    msg = f"Error loading {yaml_path}: {e}"
                    self._errors.append(msg)
                    print(f"  ! {msg}", file=sys.stderr)

    # ── Dependency Detection ─────────────────────────────────────────────

    def _scan_dependencies(self, repo: RepoMetadata) -> set:
        """Scan repo for dependencies from package.json and pyproject.toml."""
        deps = set()
        if not repo.repo_path:
            return deps

        pkg = repo.repo_path / "package.json"
        if pkg.exists():
            try:
                with open(pkg, "r") as f:
                    data = json.load(f)
                for key in ("dependencies", "devDependencies"):
                    if key in data:
                        deps.update(data[key].keys())
            except (json.JSONDecodeError, OSError) as e:
                self._errors.append(f"package.json error in {repo.name}: {e}")

        pyp = repo.repo_path / "pyproject.toml"
        if pyp.exists() and tomllib is not None:
            try:
                with open(pyp, "rb") as f:
                    data = tomllib.load(f)
                poetry = data.get("tool", {}).get("poetry", {})
                if "dependencies" in poetry:
                    deps.update(poetry["dependencies"].keys())
                for group in poetry.get("group", {}).values():
                    if "dependencies" in group:
                        deps.update(group["dependencies"].keys())
            except (ValueError, OSError, KeyError) as e:
                self._errors.append(f"pyproject.toml error in {repo.name}: {e}")

        return deps

    def _collect_tech_keys(self, repo: RepoMetadata) -> set:
        """Collect all tech keys for a repo (YAML + scanned deps). Cached."""
        if repo.name in self._tech_cache:
            return self._tech_cache[repo.name]

        techs = set()
        for lang in repo.tech_stack.languages:
            techs.add(lang.lower())
        for fw in repo.tech_stack.frameworks:
            techs.add(fw.lower())
        for tool in repo.tech_stack.tools:
            techs.add(tool.lower())
        scanned = self._scan_dependencies(repo)
        techs.update(d.lower().replace("_", "").replace("-", "") for d in scanned)

        self._tech_cache[repo.name] = techs
        return techs

    # ── Badge Generation ─────────────────────────────────────────────────

    def _tech_badges(self, repo: RepoMetadata) -> List[str]:
        """Generate shields.io tech badges for a repo."""
        techs = self._collect_tech_keys(repo)
        badges = []
        for tech in sorted(techs):
            if any(p in tech for p in self.SKIP_PATTERNS):
                continue
            if tech in self.SHIELD_MAP:
                name, color, text_color = self.SHIELD_MAP[tech]
                safe_name = urlquote(name, safe="")
                safe_logo = urlquote(tech, safe="")
                badges.append(
                    f"![{name}](https://img.shields.io/badge/{safe_name}-{color}"
                    f"?style=flat-square&logo={safe_logo}&logoColor={text_color})"
                )
        return badges

    def _status_badge(self, status: str) -> str:
        """Small shields.io status badge."""
        label, color = self.STATUS_CONFIG.get(status, ("—", "555555"))
        return (
            f"![{label}](https://img.shields.io/badge/"
            f"{urlquote(label, safe='')}-{color}?style=flat-square)"
        )

    def _skill_icons_url(self) -> str:
        """Aggregate tech stack across all repos → skillicons.dev image tag."""
        all_techs = set()
        for repo in self.repos:
            all_techs.update(self._collect_tech_keys(repo))

        icons = []
        seen = set()
        for tech in sorted(all_techs):
            if tech in self.SKILL_ICON_MAP:
                icon = self.SKILL_ICON_MAP[tech]
                if icon not in seen:
                    icons.append(icon)
                    seen.add(icon)

        if not icons:
            return ""
        return (
            f'<img src="https://skillicons.dev/icons'
            f'?i={",".join(icons)}&theme=dark&perline=15" '
            f'alt="Tech Stack" />'
        )

    # ── Helpers ───────────────────────────────────────────────────────────

    @staticmethod
    def _escape_table_cell(text: str) -> str:
        """Escape pipe characters for markdown table cells."""
        return text.replace("|", "\\|")

    # ── Repo Splitting ───────────────────────────────────────────────────

    def _split_repos(self):
        """Split repos into featured (ordered) and catalog (alphabetical)."""
        featured_set = set(self.config.featured_repos)
        featured = []
        catalog = []
        for repo in self.repos:
            if repo.name in featured_set:
                featured.append(repo)
            else:
                catalog.append(repo)

        order = {name: i for i, name in enumerate(self.config.featured_repos)}
        featured.sort(key=lambda r: order.get(r.name, 999))
        catalog.sort(key=lambda r: r.name.lower())
        return featured, catalog

    # ── Markdown Generation ──────────────────────────────────────────────

    def generate_markdown(self) -> str:
        """Generate the complete profile README."""
        L = []  # line accumulator
        u = self.config.github_username
        featured, catalog = self._split_repos()

        # ── Header: capsule-render wave ──────────────────────────────────
        L.append(
            f'<img src="https://capsule-render.vercel.app/api'
            f"?type=waving&color=0:{self.PINK},50:{self.PURPLE},100:{self.CYAN}"
            f'&height=120&section=header" width="100%" alt="" />'
        )
        L.append("")

        # ── ASCII title + typing SVG + bio ───────────────────────────────
        L.append('<div align="center">')
        L.append("")
        L.extend([
            "```",
            "█▀▀ ▄▀█ ▀█▀ ▄▀█ █░░ █▄█ █▀ ▀█▀",
            "█▄▄ █▀█ ░█░ █▀█ █▄▄ ░█░ ▄█ ░█░",
            "```",
            "",
        ])

        if self.config.taglines:
            joined = ";".join(t.replace(" ", "+") for t in self.config.taglines)
            L.append(
                f"[![Typing SVG](https://readme-typing-svg.demolab.com"
                f"?font=Orbitron&size=20&duration=3000&pause=1000"
                f"&color={self.CYAN}&center=true&vCenter=true"
                f"&width=600&lines={joined})](https://github.com/{u})"
            )
            L.append("")

        if self.config.bio:
            L.append(f"*{self.config.bio}*")
            L.append("")

        # ── Aggregate tech strip ─────────────────────────────────────────
        icons = self._skill_icons_url()
        if icons:
            L.extend(["<br/>", "", icons, ""])

        L.extend(["</div>", "", "---", ""])

        # ── Stats: 2-column table + full-width activity graph ────────────
        L.append('<div align="center">')
        L.append("")
        L.extend([
            '<table role="presentation"><tr>',
            (
                f'<td><img src="https://streak-stats.demolab.com'
                f"?user={u}&theme=synthwave&hide_border=true"
                f"&background={self.BG}&ring={self.CYAN}"
                f"&fire={self.PINK}&currStreakLabel={self.CYAN}"
                f'&sideLabels={self.PURPLE}" alt="GitHub contribution streak stats" /></td>'
            ),
            (
                f'<td><img src="https://github-readme-stats-sigma-five.vercel.app'
                f"/api/top-langs/?username={u}&layout=compact"
                f"&theme=synthwave&hide_border=true&bg_color={self.BG}"
                f"&title_color={self.CYAN}&text_color=ffffff"
                f'&icon_color={self.PURPLE}" alt="Most used programming languages" /></td>'
            ),
            "</tr></table>",
            "",
        ])

        L.append(
            f'<img src="https://github-readme-activity-graph.vercel.app'
            f"/graph?username={u}&theme=react-dark&hide_border=true"
            f"&bg_color={self.BG}&color={self.CYAN}&line={self.PINK}"
            f'&point={self.PURPLE}&area=true&area_color={self.PINK}"'
            f' width="95%" alt="Contribution activity graph" />'
        )
        L.extend(["", "</div>", "", "---", ""])

        # ── Featured Projects ────────────────────────────────────────────
        if featured:
            L.extend(["## Featured Projects", ""])

            for repo in featured:
                badge = self._status_badge(repo.status)
                if repo.repo_url:
                    L.append(f"### [{repo.name}]({repo.repo_url})  {badge}")
                else:
                    L.append(f"### {repo.name}  {badge}")
                L.append("")

                if repo.description:
                    L.extend([f"> {repo.description}", ""])

                # Highlights only (badges removed per design review — too noisy)
                if repo.highlights:
                    for h in repo.highlights[:MAX_FEATURED_HIGHLIGHTS]:
                        L.append(f"- {h}")
                    L.append("")

                L.extend(["---", ""])

        # ── Project Catalog (collapsible) ────────────────────────────────
        if catalog:
            L.extend([
                "<details>",
                '<summary><h2>All Projects</h2></summary>',
                "",
                "| Project | Description | Stack | Status |",
                "|:--------|:------------|:------|:------:|",
            ])

            for repo in catalog:
                # Name (linked if public)
                name = (
                    f"**[{repo.name}]({repo.repo_url})**"
                    if repo.repo_url and not repo.private
                    else f"**{repo.name}**"
                )

                # Truncated + escaped description
                desc = self._escape_table_cell(repo.description)
                if len(desc) > MAX_CATALOG_DESC_LEN:
                    desc = desc[:MAX_CATALOG_DESC_LEN - 3] + "..."

                # Compact tech (just language names, no badges)
                langs = self._escape_table_cell(
                    ", ".join(repo.tech_stack.languages[:3]) or "—"
                )

                # Status
                label, color = self.STATUS_CONFIG.get(
                    repo.status, ("—", "555555")
                )
                status = f"`{label}`"

                L.append(f"| {name} | {desc} | {langs} | {status} |")

            L.extend(["", "</details>", "", "---", ""])

        # ── Footer ───────────────────────────────────────────────────────
        L.extend([
            '<div align="center">',
            "",
            "```",
            "╔══════════════════════════════════════════════════════╗",
            '║  "It works on my machine" — The Catalyst Guarantee  ║',
            "╚══════════════════════════════════════════════════════╝",
            "```",
            "",
            (
                f"**[{u}](https://github.com/{u})**"
                f" · *Making git branches drift since 2024*"
            ),
            "",
            "</div>",
            "",
            (
                f'<img src="https://capsule-render.vercel.app/api'
                f"?type=waving&color=0:{self.CYAN},50:{self.PURPLE},100:{self.PINK}"
                f'&height=100&section=footer" width="100%" alt="" />'
            ),
            "",  # trailing newline
        ])

        return "\n".join(L)

    # ── Output ───────────────────────────────────────────────────────────

    def save_readme(self, output_path: Path):
        """Atomic write: write to temp file, then rename over target."""
        content = self.generate_markdown()

        # Write to temp file in same directory (ensures same filesystem for rename)
        fd, tmp_path = tempfile.mkstemp(
            dir=output_path.parent, prefix=".readme-", suffix=".tmp"
        )
        try:
            with os.fdopen(fd, "w") as f:
                f.write(content)
            os.replace(tmp_path, output_path)
        except Exception:
            # Clean up temp file on failure
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise

        print(f"\n  README.md → {output_path}")


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    config_path = script_dir / "config.yml"

    print()
    print("  GitHub Profile Generator v2.1")
    print("  ─────────────────────────────")
    print()

    try:
        with open(config_path, "r") as f:
            config = Config(**yaml.safe_load(f))
            print(f"  Config: {config_path}")
    except Exception as e:
        print(f"  Error: {e}", file=sys.stderr)
        sys.exit(1)

    print()

    gen = ProfileGenerator(config, script_dir)
    gen.scan_repositories()

    print(f"\n  Found {len(gen.repos)} repositories")

    if gen._errors:
        print(f"  Warnings: {len(gen._errors)}", file=sys.stderr)
        for err in gen._errors:
            print(f"    - {err}", file=sys.stderr)

    gen.save_readme(repo_root / "README.md")

    print()
    print("  Done.")
    print()

    # Non-zero exit if there were errors
    if gen._errors:
        sys.exit(0)  # warnings only, still succeed


if __name__ == "__main__":
    main()
