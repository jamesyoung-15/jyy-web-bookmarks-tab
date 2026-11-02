from pathlib import Path

from bookmarks_page.cli import main
from bookmarks_page.export import parse_export
from bookmarks_page.notes import load_notes, parse_notes
from bookmarks_page.page import build_page_data, render_layouts

EXPORT = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<DL><p>
    <DT><H3 PERSONAL_TOOLBAR_FOLDER="true">Bookmarks Bar</H3>
    <DL><p>
        <DT><H3>essentials</H3>
        <DL><p>
            <DT><A HREF="https://a.example.com/x" ADD_DATE="100" ICON="data:image/png;base64,AA">A</A>
        </DL><p>
        <DT><H3>tools</H3>
        <DL><p>
            <DT><A HREF="https://a.example.com/x">A again</A>
            <DT><A HREF="https://b.example.com/">B &amp; co</A>
            <DT><H3>nested</H3>
            <DL><p>
                <DT><A HREF="https://c.example.com/" ICON="https://evil.example/i.png">C</A>
            </DL><p>
        </DL><p>
        <DT><A HREF="javascript:alert(1)">bookmarklet</A>
        <DT><A HREF="https://loose.example.com/">Loose</A>
    </DL><p>
</DL><p>
"""

NOTES = """
[settings]
pinned = "essentials"

[[link]]
url = "https://b.example.com/"
desc = "Bee </script> tool"
tags = ["one", "two"]
alias = "bee"
"""


def test_parse_export_folders_and_filters():
    bms = parse_export(EXPORT)
    assert [(b.folders, b.title) for b in bms] == [
        (("essentials",), "A"),
        (("tools",), "A again"),
        (("tools",), "B & co"),
        (("tools", "nested"), "C"),
        ((), "Loose"),
    ]
    assert bms[0].icon.startswith("data:image/")
    assert bms[0].added == 100
    assert bms[3].icon == "", "non-data icons are dropped so the page never fetches"


def test_build_dedupes_and_merges_notes():
    data = build_page_data(parse_export(EXPORT), parse_notes(NOTES), "x.html")
    assert len(data.links) == 4
    assert [g.name for g in data.groups] == ["tools", "tools / nested", "unsorted"]
    a = data.links[data.pinned[0]]
    assert a.title == "A"
    assert a.groups == ["essentials", "tools"]
    b = next(link for link in data.links.values() if link.host == "b.example.com")
    assert (b.desc, b.tags, b.alias) == ("Bee </script> tool", ["one", "two"], "bee")


def test_render_escapes_script_close(tmp_path: Path):
    data = build_page_data(parse_export(EXPORT), parse_notes(NOTES), "x.html")
    written = render_layouts(data, tmp_path)
    assert {p.name for p in written} >= {"cards.html"}
    html = (tmp_path / "cards.html").read_text()
    assert "Bee <\\/script> tool" in html
    assert "/*__DATA__*/" not in html


def test_cli_init_notes_appends_stubs(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "export.html").write_text(EXPORT)
    main(["export.html", "--init-notes"])
    notes = load_notes(tmp_path / "notes.toml")
    assert len(notes.links) == 4
    assert notes.settings.pinned == "essentials"
    main(["export.html", "--init-notes"])
    assert "every link already has an entry" in capsys.readouterr().out
    assert (tmp_path / "dist" / "cards.html").exists()


def test_notes_survive_reexport(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "old.html").write_text(EXPORT)
    main(["old.html", "--init-notes"])
    notes_file = tmp_path / "notes.toml"
    notes_file.write_text(
        notes_file.read_text().replace(
            'url = "https://b.example.com/"\ndesc = ""',
            'url = "https://b.example.com/"\ndesc = "kept"',
        )
    )
    # New export: B renamed, C removed, D added.
    new = (
        EXPORT.replace("B &amp; co", "B renamed")
        .replace('<DT><A HREF="https://c.example.com/" ICON="https://evil.example/i.png">C</A>', "")
        .replace("Loose</A>", 'Loose</A>\n<DT><A HREF="https://d.example.com/">D</A>')
    )
    (tmp_path / "new.html").write_text(new)
    capsys.readouterr()
    main(["new.html", "--init-notes"])
    out = capsys.readouterr().out
    notes = load_notes(notes_file)
    assert notes.links["https://b.example.com/"].desc == "kept"
    assert "https://d.example.com/" in notes.links
    assert "orphan:  notes entry not in export: https://c.example.com/" in out
