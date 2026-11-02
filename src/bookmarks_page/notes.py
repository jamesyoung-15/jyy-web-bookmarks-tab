"""Load and extend ``notes.toml``, the per-link info Chrome cannot store."""

import json
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

NOTES_HEADER = """\
# Extra info for bookmarks, matched to the Chrome export by exact URL.
# Every field except url is optional. Rebuild after editing.

[settings]
title = "Bookmarks"
pinned = "essentials"        # folder shown as the pinned row
hide_pinned_group = true     # do not also render it as a normal group
group_order = []             # e.g. ["openshift", "vsphere"]; unlisted groups follow
"""


@dataclass(frozen=True)
class Settings:
    """Page-wide options from the ``[settings]`` table."""

    title: str = "Bookmarks"
    pinned: str = ""
    hide_pinned_group: bool = True
    group_order: tuple[str, ...] = ()


@dataclass(frozen=True)
class Note:
    """Extra info for one URL from a ``[[link]]`` entry."""

    url: str
    title: str = ""
    desc: str = ""
    tags: tuple[str, ...] = ()
    alias: str = ""


@dataclass(frozen=True)
class Notes:
    """Parsed ``notes.toml``."""

    settings: Settings = field(default_factory=Settings)
    links: dict[str, Note] = field(default_factory=dict)
    duplicates: tuple[str, ...] = ()


def _strings(value: Any) -> tuple[str, ...]:  # noqa: ANN401 - raw TOML value
    """Normalize a string or list of strings into a tuple without blanks."""
    if value is None:
        return ()
    items = [value] if isinstance(value, str) else list(value)
    return tuple(s for s in (str(v).strip() for v in items) if s)


def parse_notes(text: str) -> Notes:
    """Parse notes TOML text. Raises ``tomllib.TOMLDecodeError`` on bad syntax."""
    data = tomllib.loads(text)
    raw = data.get("settings", {})
    settings = Settings(
        title=str(raw.get("title", Settings.title)),
        pinned=str(raw.get("pinned", Settings.pinned)),
        hide_pinned_group=bool(raw.get("hide_pinned_group", Settings.hide_pinned_group)),
        group_order=_strings(raw.get("group_order")),
    )
    links: dict[str, Note] = {}
    duplicates: list[str] = []
    for entry in data.get("link", []):
        url = str(entry.get("url", "")).strip()
        if not url:
            continue
        if url in links:
            duplicates.append(url)
        links[url] = Note(
            url=url,
            title=str(entry.get("title", "")).strip(),
            desc=str(entry.get("desc", "")).strip(),
            tags=_strings(entry.get("tags")),
            alias=" ".join(_strings(entry.get("alias"))),
        )
    return Notes(settings=settings, links=links, duplicates=tuple(duplicates))


def load_notes(path: Path) -> Notes:
    """Load notes from ``path``, or return empty notes if it does not exist."""
    if not path.exists():
        return Notes()
    return parse_notes(path.read_text(encoding="utf-8"))


def _toml_str(s: str) -> str:
    # JSON string escapes are valid TOML basic-string escapes.
    return json.dumps(s, ensure_ascii=False)


def stub_entries(missing: list[tuple[str, str, list[str]]]) -> str:
    """Render empty ``[[link]]`` entries for (url, title, groups) tuples."""
    return "".join(
        f"\n[[link]]\n# {title} ({', '.join(groups)})\n"
        f'url = {_toml_str(url)}\ndesc = ""\ntags = []\nalias = ""\n'
        for url, title, groups in missing
    )


def append_stubs(path: Path, missing: list[tuple[str, str, list[str]]]) -> None:
    """Append stub entries to ``path``, writing the settings header if it is new."""
    header = "" if path.exists() else NOTES_HEADER
    with path.open("a", encoding="utf-8") as f:
        f.write(header + stub_entries(missing))
