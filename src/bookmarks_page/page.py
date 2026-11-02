"""Merge bookmarks with notes and render the HTML layouts."""

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from importlib.resources import files
from pathlib import Path
from urllib.parse import urlsplit

from bookmarks_page.export import RawBookmark
from bookmarks_page.notes import Notes

UNSORTED = "unsorted"


@dataclass
class Link:
    """One unique URL as the page sees it."""

    id: str
    title: str
    url: str
    host: str
    icon: str
    desc: str
    tags: list[str]
    alias: str
    added: int
    groups: list[str] = field(default_factory=list)


@dataclass
class Group:
    """A folder shown on the page, holding link ids in export order."""

    name: str
    links: list[str]


@dataclass
class PageData:
    """Everything the page script needs, serialized as JSON into each layout."""

    title: str
    source: str
    generated: str
    pinned: list[str]
    pinned_name: str
    groups: list[Group]
    links: dict[str, Link]

    def to_json(self) -> str:
        """Serialize for embedding inside a ``<script>`` block."""
        data = asdict(self)
        data["pinnedName"] = data.pop("pinned_name")
        # Keep the JSON from closing the <script> block early.
        return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def build_page_data(bookmarks: list[RawBookmark], notes: Notes, source: str) -> PageData:
    """Deduplicate bookmarks by URL, group them by folder, and attach notes."""
    by_url: dict[str, Link] = {}
    groups: dict[str, list[str]] = {}
    for bm in bookmarks:
        group = " / ".join(bm.folders) or UNSORTED
        urls = groups.setdefault(group, [])
        if bm.url not in urls:
            urls.append(bm.url)
        if bm.url in by_url:
            if group not in by_url[bm.url].groups:
                by_url[bm.url].groups.append(group)
            continue
        note = notes.links.get(bm.url)
        host = urlsplit(bm.url).hostname or ""
        by_url[bm.url] = Link(
            id=f"l{len(by_url)}",
            title=(note and note.title) or bm.title or host or bm.url,
            url=bm.url,
            host=host,
            icon=bm.icon,
            desc=note.desc if note else "",
            tags=list(note.tags) if note else [],
            alias=note.alias if note else "",
            added=bm.added,
            groups=[group],
        )

    settings = notes.settings
    order = [g for g in settings.group_order if g in groups]
    names = order + [g for g in groups if g not in order]
    if settings.hide_pinned_group:
        names = [g for g in names if g != settings.pinned]

    return PageData(
        title=settings.title,
        source=source,
        generated=datetime.now().isoformat(timespec="minutes"),
        pinned=[by_url[u].id for u in groups.get(settings.pinned, [])],
        pinned_name=settings.pinned,
        groups=[Group(name=g, links=[by_url[u].id for u in groups[g]]) for g in names],
        links={link.id: link for link in by_url.values()},
    )


def render_layouts(data: PageData, out_dir: Path) -> list[Path]:
    """Write one self-contained HTML file per layout template into ``out_dir``."""
    templates = files("bookmarks_page") / "templates"
    css = (templates / "_shared.css").read_text(encoding="utf-8")
    js = (templates / "_shared.js").read_text(encoding="utf-8")
    payload = data.to_json()
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for tpl in sorted(templates.iterdir(), key=lambda t: t.name):
        if not tpl.name.endswith(".html") or tpl.name.startswith("_"):
            continue
        html = (
            tpl.read_text(encoding="utf-8")
            .replace("/*__CSS__*/", css)
            .replace("/*__JS__*/", js)
            .replace("/*__DATA__*/", payload)
            .replace("__TITLE__", data.title)
        )
        path = out_dir / tpl.name
        path.write_text(html, encoding="utf-8")
        written.append(path)
    return written
