"""
Tests for the GitHub Profile Generator.

Tier 1: Unit tests for badge generation, repo splitting, escaping, truncation.
Tier 2: Integration tests for YAML scanning (valid, malformed, extra fields, empty, hidden).
Tier 3: Smoke tests for full markdown generation (sections, URLs, HTML balance, newlines, atomic write).
"""

import os
import re
import textwrap
from pathlib import Path
from urllib.parse import urlparse

import pytest

# The module under test lives one directory up from tests/
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from generate import (
    Config,
    RepoMetadata,
    TechStack,
    ProfileGenerator,
    MAX_CATALOG_DESC_LEN,
)


# ── Helpers / Fixtures ───────────────────────────────────────────────────────


def _minimal_config(**overrides) -> Config:
    """Build a minimal Config, merging in any overrides."""
    defaults = {
        "scan_paths": [],
        "github_username": "testuser",
        "featured_repos": [],
    }
    defaults.update(overrides)
    return Config(**defaults)


def _minimal_repo(**overrides) -> RepoMetadata:
    """Build a minimal RepoMetadata, merging in any overrides."""
    defaults = {"name": "test-repo"}
    defaults.update(overrides)
    return RepoMetadata(**defaults)


def _make_generator(config: Config = None, repos: list = None) -> ProfileGenerator:
    """Create a ProfileGenerator with optional pre-loaded repos."""
    if config is None:
        config = _minimal_config()
    gen = ProfileGenerator(config, Path("/tmp/fake-script-dir"))
    if repos is not None:
        gen.repos = repos
    return gen


# ── Tier 1: Unit Tests ──────────────────────────────────────────────────────


class TestTechBadges:
    """Unit tests for _tech_badges()."""

    def test_tech_badges_known_tech(self):
        """Known SHIELD_MAP entry produces a correct shields.io URL."""
        repo = _minimal_repo(
            tech_stack=TechStack(languages=["python"]),
        )
        gen = _make_generator()
        badges = gen._tech_badges(repo)

        assert len(badges) == 1
        badge = badges[0]
        assert "img.shields.io/badge/" in badge
        assert "Python" in badge
        assert "3776AB" in badge  # Python color
        assert "logo=python" in badge

    def test_tech_badges_unknown_tech(self):
        """Unknown tech is silently skipped — no badge produced."""
        repo = _minimal_repo(
            tech_stack=TechStack(languages=["brainfuck"]),
        )
        gen = _make_generator()
        badges = gen._tech_badges(repo)

        assert badges == []

    def test_tech_badges_skip_patterns(self):
        """Entries matching SKIP_PATTERNS are excluded from badges."""
        repo = _minimal_repo(
            tech_stack=TechStack(
                tools=["eslint", "babel", "@types/node", "plugin-foo"],
            ),
        )
        gen = _make_generator()
        badges = gen._tech_badges(repo)

        # All four should be filtered out by SKIP_PATTERNS
        assert badges == []

    def test_tech_badges_url_encoding(self):
        """Badge names with special characters are properly URL-encoded."""
        # "Argo CD" has a space — verify it becomes "Argo%20CD" in the URL
        repo = _minimal_repo(
            tech_stack=TechStack(tools=["argocd"]),
        )
        gen = _make_generator()
        badges = gen._tech_badges(repo)

        assert len(badges) == 1
        badge = badges[0]
        # The label "Argo CD" should be URL-encoded
        assert "Argo%20CD" in badge


class TestStatusBadge:
    """Unit tests for _status_badge()."""

    def test_status_badge_all_statuses(self):
        """Each STATUS_CONFIG entry renders a well-formed badge."""
        gen = _make_generator()

        for status, (label, color) in ProfileGenerator.STATUS_CONFIG.items():
            badge = gen._status_badge(status)
            assert "img.shields.io/badge/" in badge
            assert color in badge
            assert f"![{label}]" in badge

    def test_status_badge_unknown(self):
        """An unrecognized status falls back to the default dash/grey."""
        gen = _make_generator()
        badge = gen._status_badge("totally-unknown-status")

        # Default: label "—", color "555555"
        assert "555555" in badge
        # The dash may be URL-encoded
        assert "![" in badge


class TestSplitRepos:
    """Unit tests for _split_repos()."""

    def test_split_repos_ordering(self):
        """Featured repos respect config order; catalog is alphabetical."""
        config = _minimal_config(
            featured_repos=["charlie", "alpha"],
        )
        repos = [
            _minimal_repo(name="bravo"),
            _minimal_repo(name="alpha"),
            _minimal_repo(name="delta"),
            _minimal_repo(name="charlie"),
        ]
        gen = _make_generator(config=config, repos=repos)
        featured, catalog = gen._split_repos()

        # Featured order matches config order, not insertion order
        assert [r.name for r in featured] == ["charlie", "alpha"]

        # Catalog is everything else, sorted alphabetically
        assert [r.name for r in catalog] == ["bravo", "delta"]


class TestEscapeTableCell:
    """Unit tests for _escape_table_cell()."""

    def test_escape_table_cell(self):
        """Pipe characters are escaped for markdown tables."""
        assert ProfileGenerator._escape_table_cell("a | b | c") == "a \\| b \\| c"

    def test_escape_table_cell_no_pipes(self):
        """Text without pipes passes through unchanged."""
        assert ProfileGenerator._escape_table_cell("hello world") == "hello world"


class TestDescriptionTruncation:
    """Unit tests for description truncation in the catalog table."""

    def test_description_truncation(self):
        """Long descriptions are truncated with '...' in the catalog."""
        long_desc = "A" * 200
        config = _minimal_config(featured_repos=[])
        repo = _minimal_repo(name="longdesc-repo", description=long_desc)
        gen = _make_generator(config=config, repos=[repo])

        md = gen.generate_markdown()

        # The catalog table row should contain the truncated description
        # MAX_CATALOG_DESC_LEN - 3 chars + "..."
        truncated = "A" * (MAX_CATALOG_DESC_LEN - 3) + "..."
        assert truncated in md

        # The full 200-char description should NOT appear
        assert long_desc not in md


# ── Tier 2: Integration Tests ───────────────────────────────────────────────


class TestScanRepositories:
    """Integration tests for scan_repositories() using temp directories."""

    def _write_yaml(self, path: Path, content: str):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def test_scan_valid_repo(self, tmp_path):
        """A directory with a valid catalyst_repo.yaml is discovered."""
        repo_dir = tmp_path / "my-project"
        repo_dir.mkdir()
        self._write_yaml(
            repo_dir / "catalyst_repo.yaml",
            textwrap.dedent("""\
                name: my-project
                description: A test project
                status: active
                tech_stack:
                  languages:
                    - python
                groups:
                  - testing
            """),
        )

        config = _minimal_config(scan_paths=[str(tmp_path)])
        gen = ProfileGenerator(config, Path("/"))  # script_dir=/ so scan_path is absolute
        gen.scan_repositories()

        assert len(gen.repos) == 1
        assert gen.repos[0].name == "my-project"
        assert gen.repos[0].status == "active"
        assert gen._errors == []

    def test_scan_malformed_yaml(self, tmp_path):
        """Malformed YAML logs error, doesn't crash, appends to _errors."""
        repo_dir = tmp_path / "bad-yaml"
        repo_dir.mkdir()
        self._write_yaml(
            repo_dir / "catalyst_repo.yaml",
            "name: [invalid yaml\n  broken: {{\n",
        )

        config = _minimal_config(scan_paths=[str(tmp_path)])
        gen = ProfileGenerator(config, Path("/"))
        gen.scan_repositories()

        assert len(gen.repos) == 0
        assert len(gen._errors) == 1
        assert "YAML parse error" in gen._errors[0] or "Error loading" in gen._errors[0]

    def test_scan_extra_fields(self, tmp_path):
        """YAML with unknown fields is handled via extra='ignore'."""
        repo_dir = tmp_path / "extra-fields"
        repo_dir.mkdir()
        self._write_yaml(
            repo_dir / "catalyst_repo.yaml",
            textwrap.dedent("""\
                version: "0.1.1"
                name: extra-fields
                description: Has extra fields
                status: wip
                ml:
                  framework: pytorch
                  gpu: true
                custom_stuff:
                  - one
                  - two
            """),
        )

        config = _minimal_config(scan_paths=[str(tmp_path)])
        gen = ProfileGenerator(config, Path("/"))
        gen.scan_repositories()

        assert len(gen.repos) == 1
        assert gen.repos[0].name == "extra-fields"
        assert gen._errors == []

    def test_scan_empty_yaml(self, tmp_path):
        """Empty YAML file is skipped (not crashed)."""
        repo_dir = tmp_path / "empty"
        repo_dir.mkdir()
        self._write_yaml(repo_dir / "catalyst_repo.yaml", "")

        config = _minimal_config(scan_paths=[str(tmp_path)])
        gen = ProfileGenerator(config, Path("/"))
        gen.scan_repositories()

        assert len(gen.repos) == 0
        assert gen._errors == []

    def test_scan_hidden_repo(self, tmp_path):
        """Repos in hidden_repos list are excluded."""
        for name in ["visible-repo", "secret-repo"]:
            repo_dir = tmp_path / name
            repo_dir.mkdir()
            self._write_yaml(
                repo_dir / "catalyst_repo.yaml",
                f"name: {name}\ndescription: test\n",
            )

        config = _minimal_config(
            scan_paths=[str(tmp_path)],
            hidden_repos=["secret-repo"],
        )
        gen = ProfileGenerator(config, Path("/"))
        gen.scan_repositories()

        names = [r.name for r in gen.repos]
        assert "visible-repo" in names
        assert "secret-repo" not in names


# ── Tier 3: Smoke Tests ─────────────────────────────────────────────────────


@pytest.fixture
def full_generator(tmp_path):
    """Build a generator with a realistic set of fixture repos."""
    repos_data = [
        {
            "name": "alpha-project",
            "description": "The alpha project",
            "repo_url": "https://github.com/testuser/alpha-project",
            "status": "active",
            "tech_stack": {"languages": ["python", "typescript"], "frameworks": ["react"], "tools": ["docker"]},
            "groups": ["web"],
            "highlights": ["Highlight one", "Highlight two"],
        },
        {
            "name": "beta-project",
            "description": "The beta project",
            "repo_url": "https://github.com/testuser/beta-project",
            "status": "wip",
            "tech_stack": {"languages": ["go"], "frameworks": [], "tools": ["kubernetes"]},
            "groups": ["infra"],
        },
        {
            "name": "gamma-project",
            "description": "The gamma project with a much longer description that should not be truncated in featured but might be in catalog mode if it exceeds the limit",
            "repo_url": "https://github.com/testuser/gamma-project",
            "status": "experimental",
            "tech_stack": {"languages": ["rust"], "frameworks": [], "tools": []},
            "groups": ["systems"],
        },
    ]

    config = _minimal_config(
        featured_repos=["alpha-project"],
        github_username="testuser",
        display_name="Test User",
        role="Engineer",
        taglines=["Building things", "Breaking things"],
        bio="A test bio.",
        contact_links={"GitHub": "https://github.com/testuser"},
    )

    repos = [_minimal_repo(**d) for d in repos_data]
    gen = _make_generator(config=config, repos=repos)
    return gen


class TestFullGeneration:
    """Smoke tests for complete markdown generation."""

    def test_full_generation_has_sections(self, full_generator):
        """Generated markdown contains expected sections and capsule-render URLs."""
        md = full_generator.generate_markdown()

        assert "## Featured Projects" in md
        assert "<details>" in md
        assert "capsule-render.vercel.app/api" in md
        assert "alpha-project" in md
        assert "beta-project" in md
        assert "gamma-project" in md

    def test_generated_urls_well_formed(self, full_generator):
        """All URLs extracted from output are well-formed."""
        md = full_generator.generate_markdown()

        # Extract all URLs (http/https) from markdown
        url_pattern = re.compile(r'https?://[^\s)"\'><]+')
        urls = url_pattern.findall(md)

        assert len(urls) > 0, "Expected at least one URL in generated markdown"

        for url in urls:
            parsed = urlparse(url)
            assert parsed.scheme in ("http", "https"), f"Bad scheme in URL: {url}"
            assert parsed.netloc, f"Missing netloc in URL: {url}"

    def test_generated_html_tags_balanced(self, full_generator):
        """Every <div>, <table>, <details> has a matching close tag."""
        md = full_generator.generate_markdown()

        tags_to_check = ["div", "table", "details", "tr", "td", "summary"]
        for tag in tags_to_check:
            opens = len(re.findall(rf"<{tag}[\s>]", md, re.IGNORECASE))
            closes = len(re.findall(rf"</{tag}>", md, re.IGNORECASE))
            assert opens == closes, (
                f"Unbalanced <{tag}>: {opens} opens vs {closes} closes"
            )

    def test_trailing_newline(self, full_generator):
        """Output ends with a newline character."""
        md = full_generator.generate_markdown()
        assert md.endswith("\n")

    def test_atomic_write(self, full_generator, tmp_path):
        """save_readme writes atomically (temp file + rename, no partial writes)."""
        output_path = tmp_path / "README.md"

        full_generator.save_readme(output_path)

        assert output_path.exists()
        content = output_path.read_text()

        # Verify the content matches what generate_markdown produces
        assert content == full_generator.generate_markdown()

        # Verify no leftover temp files in the directory
        tmp_files = list(tmp_path.glob(".readme-*.tmp"))
        assert tmp_files == [], f"Leftover temp files found: {tmp_files}"
