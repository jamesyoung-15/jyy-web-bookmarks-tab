# Journal

Format: `YYYY-MM-DD  tag  one line`. Append only. Tags: `fail`, `why`, `found`, `wrong`.

2026-11-02  found  Chrome export has 22 bookmark entries but 19 unique URLs; `essentials` repeats links from other folders, so links are deduped by URL
2026-11-02  why    Python build + notes.toml keyed by URL over in-page localStorage importer, see docs/adr/0001
2026-11-02  why    Pinned-folder links can exist only in the pinned row, so cards layout filters the pinned row during search instead of hiding it (otherwise Enter opened an invisible match)
2026-11-02  fail   System chromium/firefox headless crashed with GLIBC_2.43 error; cause was shell LD_LIBRARY_PATH pointing at alsa-lib, `env -u LD_LIBRARY_PATH` fixes it
2026-11-02  fail   puppeteer's downloaded chrome-headless-shell does not run on NixOS (missing libglib); use system chromium via puppeteer-core executablePath
2026-11-02  found  Chrome only lets extensions replace the New Tab page; a file:// page works as startup page or home button only
2026-11-02  why    User picked the cards layout; tiles and launcher kept for now but cards is the one to maintain
2026-11-02  why    Python moved to a uv package (src/bookmarks_page, ruff, pytest, type hints) at user request; build.py removed
2026-11-02  found  The only description filled in was for AAP, a pinned-only link, and pinned chips showed desc only as a hover tooltip, so it looked like descriptions did nothing
2026-11-02  why    Cards info uses a separate (i) button beside each link plus a "Details: all" toggle, so a plain click on the link still navigates; nesting a button inside the <a> is invalid HTML
2026-11-02  fail   CSS `columns` masonry rebalances when a card grows, so opening (i) moved cards between columns; replaced with JS-assigned fixed columns weighted by link count
2026-11-02  found  notes.toml survives re-export: entries are keyed by URL, --init-notes only appends, removed links become reported orphans (tests/test_build.py::test_notes_survive_reexport)
