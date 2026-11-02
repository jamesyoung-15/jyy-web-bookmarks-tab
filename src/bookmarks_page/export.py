"""Parse the Netscape bookmark file format that Chrome exports."""

from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

# Chrome's top-level containers. Their names are dropped from group paths.
ROOT_FOLDERS = frozenset({"Bookmarks Bar", "Bookmarks bar", "Other bookmarks", "Mobile bookmarks"})


@dataclass(frozen=True)
class RawBookmark:
    """One <A> entry from the export, before deduplication."""

    folders: tuple[str, ...]
    title: str
    url: str
    icon: str
    added: int


class ExportParser(HTMLParser):
    """Collect bookmarks and their folder path.

    The format is loose HTML (unclosed <DT> and <p>), so structure comes from
    <H3> (folder name) followed by <DL> (folder contents).
    """

    def __init__(self) -> None:
        super().__init__()
        self.bookmarks: list[RawBookmark] = []
        self._stack: list[str | None] = []
        self._pending_folder: str | None = None
        self._in_h3 = False
        self._anchor: dict[str, str | None] | None = None
        self._anchor_text = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Track folder headings, folder bodies, and links."""
        if tag == "h3":
            self._in_h3 = True
            self._pending_folder = ""
        elif tag == "dl":
            self._stack.append(self._pending_folder)
            self._pending_folder = None
        elif tag == "a":
            self._anchor = dict(attrs)
            self._anchor_text = ""

    def handle_endtag(self, tag: str) -> None:
        """Close folders and emit finished links."""
        if tag == "h3":
            self._in_h3 = False
        elif tag == "dl" and self._stack:
            self._stack.pop()
        elif tag == "a" and self._anchor is not None:
            self._emit(self._anchor, self._anchor_text.strip())
            self._anchor = None

    def handle_data(self, data: str) -> None:
        """Accumulate folder names and link titles."""
        if self._in_h3 and self._pending_folder is not None:
            self._pending_folder += data
        elif self._anchor is not None:
            self._anchor_text += data

    def _emit(self, attrs: dict[str, str | None], title: str) -> None:
        url = attrs.get("href") or ""
        if not url or url.startswith("javascript:"):
            return
        icon = attrs.get("icon") or ""
        added = attrs.get("add_date") or "0"
        self.bookmarks.append(
            RawBookmark(
                folders=tuple(f for f in self._stack if f and f not in ROOT_FOLDERS),
                title=title,
                url=url,
                icon=icon if icon.startswith("data:image/") else "",
                added=int(added) if added.isdigit() else 0,
            )
        )


def parse_export(text: str) -> list[RawBookmark]:
    """Return every bookmark in an export, in file order."""
    parser = ExportParser()
    parser.feed(text)
    parser.close()
    return parser.bookmarks


def latest_export(directory: Path) -> Path | None:
    """Return the most recently modified .html file in ``directory``, if any."""
    candidates = sorted(directory.glob("*.html"), key=lambda p: p.stat().st_mtime)
    return candidates[-1] if candidates else None
