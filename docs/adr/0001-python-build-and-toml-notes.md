# 0001: Python build script with a TOML notes sidecar keyed by URL

- Status: accepted
- Date: 2026-11-02

## Context

The page must be built from a Chrome bookmarks export, and Chrome stays the source of truth. Links also need descriptions, tags, and search aliases, which Chrome bookmarks cannot hold. The work laptop has Python and Node.

## Decision

- A uv-managed package, `bookmarks_page` (standard library only at runtime; ruff and pytest for development), parses the export and writes self-contained HTML per layout into `dist/`.
- Extra per-link info lives in `notes.toml`, matched to bookmarks by exact URL. The build reports links without notes and notes whose URL left the export.

## Alternatives rejected

- In-page importer that stores data in localStorage: data lives in one browser profile and is lost when site data is cleared.
- Encoding descriptions in bookmark titles (`Name | desc`): clutters the Chrome bookmark bar and has no room for tags.
- Matching notes by title: titles change more often than URLs, and two bookmarks can share one title.

## Consequences

- Changing a URL in Chrome orphans its notes entry until `url` is updated. The build lists orphans so they are easy to find.
- Requires Python 3.11+ for `tomllib`; uv provides it.
- `uv sync` on the work laptop needs access to PyPI (or a mirror) for the `uv_build` backend and dev tools.
