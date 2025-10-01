# GitHub Profile Page Generator

A synthwave-style GitHub profile README generator that scans your workspace repositories and creates a visually stunning profile page.

## Features

- 🎨 **Synthwave aesthetic** with retro ASCII art
- 📊 **GitHub stats integration** via github-readme-stats
- 🏷️ **Auto-generated badges** for stars, issues, PRs, and tech stack
- 📁 **Category grouping** for organized project display
- 🔧 **YAML-based configuration** for each repository

## Setup

### 1. Install Poetry

```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Or via pip
pip install poetry
```

### 2. Install Dependencies

```bash
# From .bin directory
poetry install

# Or from anywhere
poetry install --directory /path/to/@TheBranchDriftCatalyst/.bin
```

### 3. Configure Scan Paths

Edit `.bin/config.yml` to set your workspace paths:

```yaml
scan_paths:
  - "../.."  # workspace/ directory
  - "../../../catalyst"  # catalyst/ core directory

github_username: "YourGitHubUsername"
```

### 4. Configure Repositories

Each repository in your workspace should have a `catalyst_repo.yaml` file with the following structure:

```yaml
# Repository Information
name: "project-name"
description: "Brief description of the project"
repo_url: "https://github.com/username/repo"

# Visibility
private: false

# Repository Status (active, archived, wip, experimental)
status: "active"

# Tech Stack
tech_stack:
  languages:
    - "python"
    - "javascript"
  frameworks:
    - "flask"
    - "react"
  tools:
    - "docker"

# Grouping/Categories
groups:
  - "web-apps"
  - "api"

# Badge Configuration
badges:
  stars: true
  issues: true
  prs: true
  license: true

# Custom highlights
highlights:
  - "Featured in Product Hunt"
  - "1000+ users"
```

### 5. Generate Profile Page

Run the generator script:

```bash
# Using bash script (recommended)
./.bin/generate.sh

# Or directly with Poetry
poetry run --directory .bin python generate.py

# Or activate Poetry shell first
poetry shell
python generate.py
```

The generated `README.md` will be created in the project root.

## Configuration

The `.bin/config.yml` file supports:

- **scan_paths**: List of directories to scan for `catalyst_repo.yaml` files
- **github_username**: Your GitHub username for stats widgets
- **category_order**: (Optional) Custom ordering for project categories
- **hidden_repos**: (Optional) List of repo names to exclude from the profile
- **waka_time**: (Optional) WakaTime integration settings

## Directory Structure

```
@TheBranchDriftCatalyst/
├── .bin/
│   ├── generate.sh          # Convenience script
│   └── config.yml           # Generator config (deprecated)
├── generate.py              # Main generator script
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Poetry config
└── README.md               # Generated output
```

## Workspace Structure

The generator expects your workspace to be structured as:

```
catalyst-devspace/
└── workspace/
    ├── @project-one/
    │   └── catalyst_repo.yaml
    ├── @project-two/
    │   └── catalyst_repo.yaml
    └── @TheBranchDriftCatalyst/
        └── generate.py
```

## Customization

### Adding Categories

Categories are automatically generated from the `groups` field in `catalyst_repo.yaml`. Repositories can belong to multiple groups.

### Styling

The synthwave theme uses:
- Pink (#ff69b4) for titles
- Cyan (#00d9ff) for accents
- Purple (#bd93f9) for highlights
- Dark background (#0d1117)

### GitHub Stats

The generator uses [github-readme-stats](https://github.com/anuraghazra/github-readme-stats) for dynamic stats. Customize by modifying the URLs in `generate_markdown()` method.

## Future Enhancements (v2)

- [ ] AI-powered project summaries
- [ ] WakaTime integration
- [ ] Contribution graph
- [ ] Auto-deployment via GitHub Actions
- [ ] Theme customization options

## License

Part of the Catalyst workspace toolkit by TheBranchDriftCatalyst
