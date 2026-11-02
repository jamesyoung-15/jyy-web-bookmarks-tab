"""Command-line entry point: ``uv run bookmarks-page [EXPORT]``."""

import argparse
import sys
import tomllib
from pathlib import Path

from bookmarks_page.export import latest_export, parse_export
from bookmarks_page.notes import Notes, append_stubs, load_notes
from bookmarks_page.page import PageData, build_page_data, render_layouts


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        prog="bookmarks-page",
        description="Build static start pages from a Chrome bookmarks export.",
    )
    ap.add_argument(
        "export",
        nargs="?",
        type=Path,
        help="Chrome bookmarks export (.html); defaults to the newest in references/",
    )
    ap.add_argument("--notes", type=Path, default=Path("notes.toml"), help="notes file")
    ap.add_argument("--out", type=Path, default=Path("dist"), help="output directory")
    ap.add_argument(
        "--init-notes",
        action="store_true",
        help="append empty notes entries for links that have none",
    )
    return ap.parse_args(argv)


def _load_notes_or_exit(path: Path) -> Notes:
    try:
        return load_notes(path)
    except tomllib.TOMLDecodeError as e:
        sys.exit(f"error: {path}: {e}")


def _display(path: Path) -> str:
    """Show ``path`` relative to the working directory when possible."""
    resolved = path.resolve()
    cwd = Path.cwd()
    return str(resolved.relative_to(cwd)) if resolved.is_relative_to(cwd) else str(resolved)


def _report(data: PageData, notes: Notes, written: list[Path]) -> None:
    links = list(data.links.values())
    pinned = f", {len(data.pinned)} pinned from '{data.pinned_name}'" if data.pinned else ""
    print(f"source:  {data.source}")
    print(f"links:   {len(links)} unique in {len(data.groups)} groups{pinned}")
    print(f"wrote:   {', '.join(_display(p) for p in written)}")
    if no_desc := sum(1 for link in links if not link.desc):
        print(f"no desc: {no_desc} links without a description in the notes file")
    for url in notes.duplicates:
        print(f"warning: duplicate notes entry, last one wins: {url}")
    urls = {link.url for link in links}
    for url in notes.links:
        if url not in urls:
            print(f"orphan:  notes entry not in export: {url}")


def main(argv: list[str] | None = None) -> None:
    """Build every layout from the export and notes file."""
    args = _parse_args(argv)
    export: Path | None = args.export or latest_export(Path("references"))
    if export is None:
        sys.exit("error: no export given and none found in references/")

    bookmarks = parse_export(export.read_text(encoding="utf-8"))
    notes = _load_notes_or_exit(args.notes)

    if args.init_notes:
        data = build_page_data(bookmarks, notes, export.name)
        missing = [
            (link.url, link.title, link.groups)
            for link in data.links.values()
            if link.url not in notes.links
        ]
        if missing:
            append_stubs(args.notes, missing)
            print(f"notes:   appended {len(missing)} empty entries to {_display(args.notes)}")
            notes = _load_notes_or_exit(args.notes)
        else:
            print("notes:   every link already has an entry")

    data = build_page_data(bookmarks, notes, export.name)
    written = render_layouts(data, args.out)
    _report(data, notes, written)


if __name__ == "__main__":
    main()
