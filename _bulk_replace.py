"""Bulk find/replace + page rename for Heritage Springs Lakes Paving Co & Pergolas scaffold."""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SELF_NAME = Path(__file__).name

REPLACEMENTS = [
    ("https://geelongroofrestorations.com.au", "https://officerpavingco.com.au"),
    ("geelongroofrestorations.com.au", "officerpavingco.com.au"),
    ("geelongroofrestorations", "officerpavingco"),
    ("Geelong Roof Restorations", "Heritage Springs Lakes Paving Co &amp; Pergolas"),
    ("Geelong roof restoration", "Officer decking &amp; pergola"),
    ("Geelong&rsquo;s specialist", "Officer&rsquo;s specialist"),
    ("Geelong&rsquo;s", "Officer&rsquo;s"),
    ("Greater Geelong", "Heritage Springs Shire"),
    ("Surf Coast Shire", "Heritage Springs Hills"),
    ("Bellarine", "Heritage Springs Lakes"),
    ("Surf Coast", "Heritage Springs Hills"),
    ("Geelong, the Bellarine and the Surf Coast", "Officer, Heritage Springs Lakes and the Heritage Springs Hills"),
    ("Geelong, the Bellarine, and the Surf Coast", "Officer, Heritage Springs Lakes, and the Heritage Springs Hills"),
    ("Bell Park", "Nar Nar Goon"),
    ("Corio", "Garfield"),
    ("Ocean Grove", "Emerald"),
    ("Torquay", "Gembrook"),
    ("Geelong", "Officer"),
    ('"3220"', '"3809"'),
    ("VIC 3220", "VIC 3809"),
    ("3220", "3809"),
    ("-38.1499", "-38.0731"),
    ("144.3617", "145.4144"),
    ("Roof Restoration Services", "Decking, Pergola &amp; Outdoor Living Services"),
    ("roof restoration & replacement contractors", "decking, pergola &amp; outdoor living specialists"),
    ("Roof restoration", "Decking"),
    ("roof restoration", "decking project"),
    ("Roof Restoration", "Decking"),
    ("ROOF RESTORATION", "DECKING &amp; PERGOLAS"),
    ("specialist roof restoration", "specialist decking"),
    ("free roof inspections", "free design consultations"),
    ("Free roof inspections", "Free design consultations"),
    ("Free Inspection", "Free Consultation"),
    ("free inspection", "free consultation"),
    ("RoofingContractor", "GeneralContractor"),
    ("Roof Cleaning &amp; Pressure Washing", "Timber Decking"),
    ("Roof Painting &amp; Sealing", "Composite Decking"),
    ("Tile Restoration &amp; Repointing", "Pergolas &amp; Verandas"),
    ("Metal Roof Restoration", "Alfresco &amp; Outdoor Kitchens"),
    ("Gutter Replacement", "Deck Restoration"),
    ("Roof cleaning &amp; pressure washing", "Timber decking"),
    ("Roof painting &amp; sealing", "Composite decking"),
    ("Tile restoration &amp; repointing", "Pergolas &amp; verandas"),
    ("Metal roof restoration", "Alfresco &amp; outdoor kitchens"),
    ("Gutter replacement", "Deck restoration"),
    ("Roof Cleaning", "Timber"),
    ("Roof Painting", "Composite"),
    ("Tile Restoration", "Pergolas"),
    ("Metal Restoration", "Alfresco"),
    ("/services/roof-cleaning/", "/services/timber-decking/"),
    ("/services/roof-painting/", "/services/patio-paving/"),
    ("/services/tile-restoration/", "/services/pool-surrounds/"),
    ("/services/metal-restoration/", "/services/alfresco-outdoor-kitchens/"),
    ("/services/gutter-replacement/", "/services/deck-restoration/"),
    ("/newtown/", "/cardinia-lakes/"),
    ("/belmont/", "/officer/"),
    ("/highton/", "/cockatoo/"),
    ("/armstrong-creek/", "/emerald/"),
    ("/lara/", "/officer/"),
    ("/greater-geelong/", "/cardinia-shire/"),
    ("Newtown", "Heritage Springs Lakes"),
    ("Belmont", "Officer"),
    ("Highton", "Cockatoo"),
    ("Armstrong Creek", "Emerald"),
    ("Lara", "Officer"),
    ("quotes@geelongroofrestorations.com.au", "quotes@officerpavingco.com.au"),
    (">G</text>", ">P</text>"),
]

EXTENSIONS = {".astro", ".md", ".toml", ".mjs", ".json", ".xml", ".txt", ".html", ".css", ".js"}

def patch_file(p):
    try:
        s = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    out = s
    for old, new in REPLACEMENTS:
        out = out.replace(old, new)
    if out != s:
        p.write_text(out, encoding="utf-8")
        return True
    return False

def main():
    PAGES = ROOT / "src" / "pages"
    for old, new in [
        ("newtown.astro", "officer.astro"),
        ("belmont.astro", "beaconsfield.astro"),
        ("highton.astro", "cockatoo.astro"),
        ("armstrong-creek.astro", "emerald.astro"),
        ("lara.astro", "officer-upper.astro"),
        ("greater-geelong.astro", "cardinia-shire.astro"),
    ]:
        o, n = PAGES / old, PAGES / new
        if o.exists() and not n.exists():
            o.rename(n); print(f"renamed: {old} -> {new}")

    SVC = PAGES / "services"
    for old, new in [
        ("roof-cleaning.astro", "timber-decking.astro"),
        ("roof-painting.astro", "composite-decking.astro"),
        ("tile-restoration.astro", "pergolas.astro"),
        ("metal-restoration.astro", "alfresco-outdoor-kitchens.astro"),
        ("gutter-replacement.astro", "deck-restoration.astro"),
    ]:
        o, n = SVC / old, SVC / new
        if o.exists() and not n.exists():
            o.rename(n); print(f"renamed: {old} -> {new}")

    changed = 0
    for p in ROOT.rglob("*"):
        if not p.is_file(): continue
        if p.suffix not in EXTENSIONS: continue
        if "node_modules" in p.parts or "dist" in p.parts: continue
        if p.name == SELF_NAME: continue
        if patch_file(p):
            changed += 1

    pkg = ROOT / "package.json"
    if pkg.exists():
        s = pkg.read_text(encoding="utf-8")
        s = s.replace('"name": "geelongroofrestorations"', '"name": "officerpavingco"')
        pkg.write_text(s, encoding="utf-8")

    print(f"Done. {changed} files patched.")

if __name__ == "__main__":
    main()
