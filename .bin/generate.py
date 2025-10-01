#!/usr/bin/env python3
"""
GitHub Profile Page Generator
Scans workspace repositories and generates a synthwave-style profile README
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import yaml
from collections import defaultdict
from pydantic import BaseModel, Field


class TechStack(BaseModel):
    """Technology stack information"""
    languages: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)


class BadgeConfig(BaseModel):
    """Badge display configuration"""
    stars: bool = True
    issues: bool = True
    prs: bool = True
    license: bool = True


class RepoMetadata(BaseModel):
    """Pydantic model for repository metadata from catalyst_repo.yaml"""
    name: str
    description: str = ""
    repo_url: str = ""
    private: bool = False
    status: str = "unknown"
    tech_stack: TechStack = Field(default_factory=TechStack)
    groups: List[str] = Field(default_factory=lambda: ["uncategorized"])
    badges: BadgeConfig = Field(default_factory=BadgeConfig)
    highlights: List[str] = Field(default_factory=list)
    repo_path: Optional[Path] = None

    class Config:
        arbitrary_types_allowed = True


class Config(BaseModel):
    """Configuration for the profile generator"""
    scan_paths: List[str]
    github_username: str = "TheBranchDriftCatalyst"
    waka_time: Optional[Dict[str, str]] = None
    category_order: Optional[List[str]] = None
    hidden_repos: Optional[List[str]] = None


class ProfileGenerator:
    """Generates GitHub profile README from repository metadata"""

    def __init__(self, config: Config, script_dir: Path):
        self.config = config
        self.script_dir = script_dir
        self.repos: List[RepoMetadata] = []

    def scan_repositories(self):
        """Scan configured paths for catalyst_repo.yaml files"""
        for scan_path in self.config.scan_paths:
            # Resolve path relative to script directory
            workspace_path = (self.script_dir / scan_path).resolve()

            if not workspace_path.exists():
                print(f"⚠ Skipping non-existent path: {workspace_path}")
                continue

            print(f"Scanning: {workspace_path}")

            for repo_dir in workspace_path.iterdir():
                if not repo_dir.is_dir() or repo_dir.name.startswith('.'):
                    continue

                yaml_path = repo_dir / 'catalyst_repo.yaml'
                if yaml_path.exists():
                    try:
                        with open(yaml_path, 'r') as f:
                            data = yaml.safe_load(f)
                            if data:
                                # Skip hidden repos
                                if self.config.hidden_repos and data.get('name') in self.config.hidden_repos:
                                    print(f"  ⊗ Skipped (hidden): {data.get('name', repo_dir.name)}")
                                    continue

                                # Set default name from directory if not in YAML
                                if 'name' not in data:
                                    data['name'] = repo_dir.name
                                data['repo_path'] = repo_dir
                                repo = RepoMetadata(**data)
                                self.repos.append(repo)
                                print(f"  ✓ Loaded: {repo.name}")
                    except Exception as e:
                        print(f"  ✗ Error loading {yaml_path}: {e}", file=sys.stderr)

    def group_repos_by_category(self) -> Dict[str, List[RepoMetadata]]:
        """Group repositories by their category tags"""
        grouped = defaultdict(list)

        for repo in self.repos:
            for group in repo.groups:
                grouped[group].append(repo)

        return dict(grouped)

    def generate_badge_url(self, repo: RepoMetadata, badge_type: str) -> str:
        """Generate shields.io badge URL"""
        if not repo.repo_url or repo.private:
            return ""

        # Extract owner/repo from URL
        parts = repo.repo_url.rstrip('/').split('/')
        if len(parts) < 2:
            return ""
        owner, repo_name = parts[-2], parts[-1]

        base_url = f"https://img.shields.io/github"

        if badge_type == 'stars':
            return f"{base_url}/stars/{owner}/{repo_name}?style=for-the-badge&logo=github&color=ff69b4"
        elif badge_type == 'issues':
            return f"{base_url}/issues/{owner}/{repo_name}?style=for-the-badge&logo=github&color=00d9ff"
        elif badge_type == 'prs':
            return f"{base_url}/issues-pr/{owner}/{repo_name}?style=for-the-badge&logo=github&color=bd93f9"
        elif badge_type == 'license':
            return f"{base_url}/license/{owner}/{repo_name}?style=for-the-badge&color=50fa7b"

        return ""

    def scan_dependencies(self, repo: RepoMetadata) -> set:
        """Scan repo for dependencies from package.json and pyproject.toml"""
        dependencies = set()

        if not repo.repo_path:
            return dependencies

        # Check for package.json (Node/JS projects)
        package_json = repo.repo_path / 'package.json'
        if package_json.exists():
            try:
                import json
                with open(package_json, 'r') as f:
                    data = json.load(f)
                    # Get all deps
                    for dep_type in ['dependencies', 'devDependencies']:
                        if dep_type in data:
                            dependencies.update(data[dep_type].keys())
            except Exception:
                pass

        # Check for pyproject.toml (Python/Poetry projects)
        pyproject = repo.repo_path / 'pyproject.toml'
        if pyproject.exists():
            try:
                import toml
                with open(pyproject, 'r') as f:
                    data = toml.load(f)
                    # Get poetry dependencies
                    if 'tool' in data and 'poetry' in data['tool']:
                        if 'dependencies' in data['tool']['poetry']:
                            dependencies.update(data['tool']['poetry']['dependencies'].keys())
                        if 'group' in data['tool']['poetry']:
                            for group in data['tool']['poetry']['group'].values():
                                if 'dependencies' in group:
                                    dependencies.update(group['dependencies'].keys())
            except Exception:
                pass

        return dependencies

    def generate_tech_badges(self, repo: RepoMetadata) -> List[str]:
        """Generate technology stack badges from languages + auto-detected deps"""
        badges = []

        # Shields.io badge mapping for popular frameworks/tools
        shield_mapping = {
            # Languages
            'python': ('Python', '3776AB', 'white'),
            'javascript': ('JavaScript', 'F7DF1E', 'black'),
            'typescript': ('TypeScript', '3178C6', 'white'),
            'go': ('Go', '00ADD8', 'white'),
            'rust': ('Rust', '000000', 'white'),

            # Frontend frameworks
            'react': ('React', '61DAFB', 'black'),
            'vue': ('Vue.js', '4FC08D', 'white'),
            'svelte': ('Svelte', 'FF3E00', 'white'),
            'next': ('Next.js', '000000', 'white'),
            'nuxt': ('Nuxt.js', '00DC82', 'white'),
            'vite': ('Vite', '646CFF', 'white'),
            'webpack': ('Webpack', '8DD6F9', 'black'),

            # Backend frameworks
            'django': ('Django', '092E20', 'white'),
            'flask': ('Flask', '000000', 'white'),
            'fastapi': ('FastAPI', '009688', 'white'),
            'express': ('Express', '000000', 'white'),
            'nestjs': ('NestJS', 'E0234E', 'white'),

            # Databases
            'postgresql': ('PostgreSQL', '4169E1', 'white'),
            'mongodb': ('MongoDB', '47A248', 'white'),
            'redis': ('Redis', 'DC382D', 'white'),
            'mysql': ('MySQL', '4479A1', 'white'),

            # DevOps/Tools
            'docker': ('Docker', '2496ED', 'white'),
            'kubernetes': ('Kubernetes', '326CE5', 'white'),
            'ansible': ('Ansible', 'EE0000', 'white'),
            'terraform': ('Terraform', '7B42BC', 'white'),

            # Testing
            'jest': ('Jest', 'C21325', 'white'),
            'pytest': ('Pytest', '0A9EDC', 'white'),
            'playwright': ('Playwright', '2EAD33', 'white'),

            # Other popular tools
            'tailwindcss': ('Tailwind CSS', '06B6D4', 'white'),
            'pydantic': ('Pydantic', 'E92063', 'white'),
            'pyyaml': ('PyYAML', 'CB171E', 'white'),
            'axios': ('Axios', '5A29E4', 'white'),
            'pandas': ('Pandas', '150458', 'white'),
            'numpy': ('NumPy', '013243', 'white'),
            'dagster': ('Dagster', '654FF0', 'white'),
            'neo4j': ('Neo4j', '008CC1', 'white'),
            'spacy': ('spaCy', '09A3D5', 'white'),
            'poetry': ('Poetry', '60A5FA', 'white'),
        }

        # Collect all techs (languages from YAML + scanned dependencies)
        all_techs = set()

        # Add languages from YAML
        for lang in repo.tech_stack.languages:
            all_techs.add(lang.lower())

        # Add frameworks from YAML
        for framework in repo.tech_stack.frameworks:
            all_techs.add(framework.lower())

        # Add tools from YAML
        for tool in repo.tech_stack.tools:
            all_techs.add(tool.lower())

        # Auto-detect from package files
        scanned_deps = self.scan_dependencies(repo)
        all_techs.update(dep.lower().replace('_', '').replace('-', '') for dep in scanned_deps)

        # Skip patterns for non-major dependencies
        skip_patterns = [
            '@types/',      # TypeScript type definitions
            'types/',
            'loader',       # Webpack loaders
            'plugin',       # Plugins
            'cli',          # CLI utilities
            'config',       # Config packages
            'parser',       # Parsers
            'eslint',       # Linting
            'babel',        # Transpilers
            'tslib',        # TS internals
            'core',         # Internal core packages
            'utils',        # Utility packages
            'helper',       # Helper packages
        ]

        # Generate badges only for known techs with official shields
        for tech in sorted(all_techs):
            # Skip noise patterns
            if any(pattern in tech for pattern in skip_patterns):
                continue

            # Only show if in shield_mapping (has official badge)
            if tech in shield_mapping:
                name, color, text_color = shield_mapping[tech]
                badges.append(f"![{name}](https://img.shields.io/badge/{name.replace(' ', '%20')}-{color}?style=flat-square&logo={tech}&logoColor={text_color})")

        return badges

    def generate_markdown(self) -> str:
        """Generate the complete markdown content"""
        lines = []

        # Header with synthwave styling
        lines.extend([
            '<div align="center">',
            '',
            '```',
            '█▀▀ ▄▀█ ▀█▀ ▄▀█ █░░ █▄█ █▀ ▀█▀',
            '█▄▄ █▀█ ░█░ █▀█ █▄▄ ░█░ ▄█ ░█░',
            '',
            '▀█▀ █░█ █▀▀   █▄▄ █▀█ ▄▀█ █▄░█ █▀▀ █░█',
            '░█░ █▀█ ██▄   █▄█ █▀▄ █▀█ █░▀█ █▄▄ █▀█',
            '',
            '█▀▄ █▀█ █ █▀▀ ▀█▀   █▀▀ ▄▀█ ▀█▀ ▄▀█ █░░ █▄█ █▀ ▀█▀',
            '█▄▀ █▀▄ █ █▀░ ░█░   █▄▄ █▀█ ░█░ █▀█ █▄▄ ░█░ ▄█ ░█░',
            '```',
            '',
            '### 🌊 Building tools, breaking conventions, shipping code 🚀',
            '',
            '> *"Code doesn\'t lie, but yaml sure does confuse"*',
            '',
            '</div>',
            '',
            '---',
            '',
        ])

        # GitHub Stats (no grades, we keep those private 😎)
        username = self.config.github_username
        lines.extend([
            '## 📊 Stats',
            '',
            '<div align="center">',
            '',
            # Streak stats - no grades here
            f'[![GitHub Streak](https://streak-stats.demolab.com?user={username}&theme=synthwave&hide_border=true&background=0D1117&ring=FF69B4&fire=FF69B4&currStreakLabel=00D9FF)](https://git.io/streak-stats)',
            '',
            # Top languages
            f'![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username={username}&layout=compact&theme=synthwave&hide_border=true&bg_color=0d1117&title_color=ff69b4&text_color=ffffff)',
            '',
            # Contribution graph
            f'![Activity Graph](https://github-readme-activity-graph.vercel.app/graph?username={username}&theme=synthwave&hide_border=true&bg_color=0d1117&color=ff69b4&line=00d9ff&point=bd93f9)',
            '',
            '</div>',
            '',
            '---',
            '',
        ])

        # Projects - show each repo only once with category chips
        lines.append('## 🚀 Projects')
        lines.append('')

        # Sort repos alphabetically, show each once
        for repo in sorted(self.repos, key=lambda r: r.name):
            # Show repo name as link if it has a URL
            if repo.repo_url:
                lines.append(f'### [{repo.name}]({repo.repo_url})')
            else:
                lines.append(f'### {repo.name}')
            lines.append('')

            if repo.description:
                lines.append(f'> {repo.description}')
                lines.append('')

            # Category chips
            if repo.groups:
                category_badges = [f'`{group}`' for group in repo.groups]
                lines.append('**Categories:** ' + ' '.join(category_badges))
                lines.append('')

            # Tech stack badges
            tech_badges = self.generate_tech_badges(repo)
            if tech_badges:
                lines.append(' '.join(tech_badges))
                lines.append('')

            # GitHub badges (only if repo has URL)
            if repo.repo_url:
                badge_lines = []
                if repo.badges.stars:
                    badge_url = self.generate_badge_url(repo, 'stars')
                    if badge_url:
                        badge_lines.append(f'![Stars]({badge_url})')

                if repo.badges.issues:
                    badge_url = self.generate_badge_url(repo, 'issues')
                    if badge_url:
                        badge_lines.append(f'![Issues]({badge_url})')

                if repo.badges.prs:
                    badge_url = self.generate_badge_url(repo, 'prs')
                    if badge_url:
                        badge_lines.append(f'![PRs]({badge_url})')

                if badge_lines:
                    lines.append(' '.join(badge_lines))
                    lines.append('')

            # Highlights
            if repo.highlights:
                for highlight in repo.highlights:
                    lines.append(f'- ✨ {highlight}')
                lines.append('')

            lines.append('---')
            lines.append('')

        # Footer
        lines.extend([
            '',
            '<div align="center">',
            '',
            '---',
            '',
            '```',
            '╔══════════════════════════════════════════════════════════════╗',
            '║  🤖 Auto-generated by a Python script that definitely        ║',
            '║     didn\'t take 47 refactors to get working                  ║',
            '║                                                              ║',
            '║  ☕ Powered by coffee, spite, and questionable YAML          ║',
            '║                                                              ║',
            '║  💀 "It works on my machine" - The Catalyst Guarantee™       ║',
            '╚══════════════════════════════════════════════════════════════╝',
            '```',
            '',
            '**TheBranchDriftCatalyst** | *Making git branches drift since 2024*',
            '',
            '</div>',
        ])

        return '\n'.join(lines)

    def save_readme(self, output_path: Path):
        """Save generated markdown to README.md"""
        content = self.generate_markdown()

        with open(output_path, 'w') as f:
            f.write(content)

        print(f"\n✓ README.md generated successfully at {output_path}")


def main():
    # Determine paths
    script_dir = Path(__file__).parent  # .bin/
    repo_root = script_dir.parent       # @TheBranchDriftCatalyst/
    config_path = script_dir / 'config.yml'

    print("=" * 60)
    print("GitHub Profile Page Generator v1.0")
    print("=" * 60)
    print()

    # Load configuration
    try:
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
            config = Config(**config_data)
            print(f"✓ Loaded config from {config_path}")
    except Exception as e:
        print(f"✗ Error loading config: {e}", file=sys.stderr)
        sys.exit(1)

    print()

    # Initialize generator
    generator = ProfileGenerator(config, script_dir)

    # Scan repositories
    generator.scan_repositories()

    print(f"\nFound {len(generator.repos)} repositories with metadata")

    # Generate README to repo root (dist)
    output_path = repo_root / 'README.md'
    generator.save_readme(output_path)

    print()
    print("=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == '__main__':
    main()
