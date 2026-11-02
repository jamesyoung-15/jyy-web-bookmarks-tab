# Plan: work bookmarks start page

## Context

nightTab is blocked on the work laptop, and the user wants a static start page built from Chrome's bookmark export, set as Chrome's homepage or startup page through a `file:///` URL. Chrome stays the source of truth: edit there, re-export, rebuild. The user wants several layouts to compare, and a way to attach longer descriptions to links, because the collection will grow.

Current export (`references/bookmarks_9_9_26.html`): Bookmarks Bar with 8 flat folders and 22 links. 17 links carry base64 favicons (`ICON=`). `essentials` duplicates links from other folders. Most hosts are internal (`*.ent.corp`, `*.amfam.com`), so the page must not call external favicon services.

## Approach

Python, standard library only (needs 3.11+ for `tomllib`). One build script produces three self-contained HTML files from the same data, so the comparison is fair and switching later only changes which file Chrome points at.

### Files

```
build.py                 parse export + notes, render every template in templates/
notes.toml               hand-written descriptions, tags, aliases, keyed by URL
templates/
  _shared.css / _shared.js   search, clock, theme, keyboard, favicon fallback
  cards.html             layout A
  tiles.html             layout B
  launcher.html          layout C
dist/                    build output (gitignored)
references/              Chrome exports (input)
```

### Data flow

1. `build.py references/<export>.html` parses the export with `html.parser` and produces `[{folder, links:[{title, url, icon, added}]}]`.
2. It merges `notes.toml` by exact URL.
3. It inlines the JSON plus shared CSS and JS into each template (placeholder `/*__DATA__*/`), then writes `dist/<layout>.html`.
4. Its report lists links with no notes entry, and notes entries whose URL no longer exists in the export (orphans after a URL change).

### Notes sidecar (`notes.toml`)

Chrome bookmarks have no description field, so extra info lives beside the export, keyed by URL:

```toml
[settings]
pinned = "essentials"          # folder shown as a top pinned row, not a normal group

[[link]]
url  = "https://console-openshift-console.apps.dall-oc-001-prd.ent.corp/..."
desc = "Prod OpenShift console, Dallas. Use for app deploy status and pod logs."
tags = ["k8s", "prod", "dallas"]
alias = "ocp dal"              # extra search terms
```

- Duplicate URLs, such as one link in both `essentials` and `vsphere`, share a single entry.
- `build.py --init-notes` appends stub entries for any link that has no entry yet, so filling them in is a fill-in-the-blanks job.
- Descriptions, tags, aliases, and hostnames are all searchable.

### Shared behavior (all three layouts)

- Search box focused on load (`/` refocuses). Typing filters live, Enter opens the top match, Esc clears.
- Clock and date header.
- Follows the OS light/dark theme, with a manual toggle saved in `localStorage` (wrapped in try/catch).
- Favicon comes from the embedded `ICON`. Without one, it shows a colored letter avatar. No network fetches.
- Links open in the same tab (it is a homepage). Ctrl/middle-click works normally.
- Arrow-key navigation across visible links.

### Layouts to compare

- **A. Cards:** a responsive grid of folder cards. Each row shows icon, name, and a one-line description in muted text, with the pinned row above the grid. Densest, and the descriptions are always visible.
- **B. Tiles (nightTab-like):** large icon tiles under group headings. The description appears in a hover or focus popover. Most visual, and it uses the most space.
- **C. Launcher:** search-first and minimal. Before typing, it shows the pinned row plus collapsible groups. Typing turns it into a ranked result list with full descriptions and tags. Best once the collection grows.

### Repo hygiene

- Add `dist/` to `.gitignore`. Whether to commit `references/*.html` and `notes.toml` (internal hostnames) is the user's call, and I will ask before the first commit.
- After approval: copy this plan to `docs/plan.md`, write an ADR for "Python build + TOML sidecar keyed by URL", and add JOURNAL entries per `.agents/instructions/context.md`.
- Update `README.md` with the export and rebuild steps, plus how to set the Chrome homepage or startup page.

## Verification

1. `python3 build.py references/bookmarks_9_9_26.html` reports 22 links in 8 folders, lists the stubs missing notes, and writes `dist/cards.html`, `dist/tiles.html`, and `dist/launcher.html`.
2. `python3 build.py --init-notes ...`, then fill in 2 or 3 descriptions and rebuild. The descriptions show in each layout and match in search.
3. Open each file in Chrome via `file:///` and check: favicons render, search plus Enter opens the right link, the theme toggle persists, and there are no network requests in DevTools besides the clicked link.
4. Set one as the Chrome startup page (Settings > On startup > Open a specific page) and confirm it loads.

Least confident:
- How Chrome exports nested folders (handled recursively, flattened to `parent / child` group names, but untested against a real nested export).
- Whether Chrome policy on the work laptop blocks `file:///` startup pages.
