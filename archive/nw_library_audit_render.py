#!/usr/bin/env python3
"""
Render nw_library_audit_*.csv as a Markdown table and PDF.

Usage:
  python3 nw_library_audit_render.py                   # auto-finds latest CSV
  python3 nw_library_audit_render.py my_audit.csv      # specific file
  python3 nw_library_audit_render.py --no-pdf          # Markdown only
  python3 nw_library_audit_render.py --icons           # icon PDF (✅ ❌ ⚠️)
"""

import csv
import subprocess
import sys
from pathlib import Path

# ── find input file ────────────────────────────────────────────────────────────
script_dir = Path(__file__).parent
args = sys.argv[1:]
positional = [a for a in args if not a.startswith("--")]
flags = set(a for a in args if a.startswith("--"))

if positional:
    csv_path = Path(positional[0])
else:
    candidates = sorted(script_dir.glob("nw_library_audit_*.csv"), reverse=True)
    if not candidates:
        sys.exit("No nw_library_audit_*.csv found in script directory.")
    csv_path = candidates[0]

make_pdf  = "--no-pdf" not in flags
icon_mode = "--icons" in flags

stem     = csv_path.stem
md_path  = csv_path.with_suffix(".md")
pdf_path = csv_path.with_name(stem + ("_icons" if icon_mode else "") + ".pdf")

# ── read CSV ───────────────────────────────────────────────────────────────────
with open(csv_path, newline="") as f:
    rows = list(csv.DictReader(f))

# ── icon mapping ───────────────────────────────────────────────────────────────
ICON_OK   = "✅"
ICON_WARN = "⚠️"
ICON_BAD  = "❌"
ICON_NA   = "—"

def iconify(col, val):
    v = val.strip()
    if col in ("library.properties", "Examples", "keywords.txt"):
        if v.upper() == "OK":           return ICON_OK
        if v.upper() == "MISSING":      return ICON_BAD
        if v.upper() == "UNKNOWN":      return ICON_WARN
        if v.upper().startswith("OK ("):return ICON_WARN   # OK but with caveats
        if v.upper() == "WRONG":        return ICON_BAD
        if "NOT IN" in v.upper():       return ICON_WARN   # not in examples/ folder
        if v.upper().startswith("OK"):  return ICON_OK
        return ICON_WARN
    if col == "getHeader/getString":
        if v.upper() == "IMPLEMENTED":      return ICON_OK
        if v.upper() == "NOT IMPLEMENTED":  return ICON_BAD
        if v.upper() == "PARTIAL":          return ICON_WARN
        if v.upper() == "UNKNOWN":          return ICON_WARN
        if v.upper() in ("N/A", ""):        return ICON_NA
        return ICON_WARN
    if col == "API case":
        if v.lower() == "lowercase":    return ICON_OK
        if "capital" in v.lower():      return ICON_WARN
        if v.upper() in ("N/A", ""):    return ICON_NA
        if v.upper() == "UNKNOWN":      return ICON_WARN
        return ICON_WARN
    return val  # non-status columns: pass through unchanged

# ── tier grouping ──────────────────────────────────────────────────────────────
tier_label = {
    "1": "Tier 1 — Minor fixes only",
    "2": "Tier 2 — Moderate work",
    "3": "Tier 3 — Substantial work or blocked",
}
tier_color = {"1": "#d4edda", "2": "#fff3cd", "3": "#f8d7da"}

tiers = {"1": [], "2": [], "3": []}
for row in rows:
    tiers[row["Priority tier"]].append(row)

STATUS_COLS = {"library.properties", "Examples", "keywords.txt",
               "getHeader/getString", "API case"}
COLS = ["Library", "Type", "library.properties", "Examples",
        "keywords.txt", "getHeader/getString", "API case", "Notes"]

# ── Markdown table (plain text, no icons) ─────────────────────────────────────
def md_table(rows):
    if not rows:
        return ""
    lines = ["| " + " | ".join(COLS) + " |",
             "| " + " | ".join("---" for _ in COLS) + " |"]
    for row in rows:
        cells = [row.get(c, "").replace("|", "\\|") for c in COLS]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)

md_lines = ["# NorthernWidget Library Manager Readiness Audit", "",
            f"Source: `{csv_path.name}`", ""]
for tk in ("1", "2", "3"):
    if not tiers[tk]:
        continue
    md_lines += [f"## {tier_label[tk]}", "", md_table(tiers[tk]), ""]

md_path.write_text("\n".join(md_lines))
print(f"Markdown written: {md_path}")

if not make_pdf:
    sys.exit(0)

# ── plain PDF via pandoc+pdflatex ─────────────────────────────────────────────
if not icon_mode:
    cmd = [
        "pandoc", str(md_path), "-o", str(pdf_path),
        "--pdf-engine=pdflatex",
        "-V", "geometry:margin=1.5cm",
        "-V", "fontsize=9pt",
        "-V", "papersize=a4",
        "--variable", "classoption=landscape",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"PDF written:      {pdf_path}")
    else:
        print("pandoc error:"); print(result.stderr)
    sys.exit(0)

# ── icon PDF via HTML + Chrome headless ───────────────────────────────────────
def html_table(tier_key, rows):
    bg = tier_color[tier_key]
    cells_html = []
    for row in rows:
        tds = []
        for c in COLS:
            val = row.get(c, "")
            display = iconify(c, val) if c in STATUS_COLS else val
            # tooltip shows original text for icon cells
            title = f' title="{val}"' if c in STATUS_COLS else ""
            tds.append(f"<td{title}>{display}</td>")
        margay_class = ' class="margay-dep"' if row.get("Margay dep", "").strip().lower() == "yes" else ""
        cells_html.append(f'<tr style="background:{bg}"{margay_class}>{"".join(tds)}</tr>')
    return "\n".join(cells_html)

header_cells = "".join(f"<th>{c}</th>" for c in COLS)

section_html = []
for tk in ("1", "2", "3"):
    if not tiers[tk]:
        continue
    section_html.append(f"""
    <h2>{tier_label[tk]}</h2>
    <table>
      <thead><tr>{header_cells}</tr></thead>
      <tbody>
        {html_table(tk, tiers[tk])}
      </tbody>
    </table>""")

html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>NorthernWidget Library Audit</title>
<style>
  @page {{ size: A4 landscape; margin: 1.2cm; }}
  body {{ font-family: Arial, sans-serif; font-size: 8.5pt; }}
  h1 {{ font-size: 13pt; margin-bottom: 2px; }}
  h2 {{ font-size: 10pt; margin: 10px 0 4px; }}
  table {{ border-collapse: collapse; width: 100%; table-layout: fixed; }}
  th, td {{ border: 1px solid #aaa; padding: 3px 5px; vertical-align: top;
             word-wrap: break-word; overflow-wrap: break-word; }}
  th {{ background: #343a40; color: white; font-size: 8pt; text-align: center; }}
  td:nth-child(1) {{ width: 13%; font-weight: bold; }}
  td:nth-child(2) {{ width: 6%; }}
  td:nth-child(3), td:nth-child(4), td:nth-child(5) {{ width: 7%; text-align: center; }}
  td:nth-child(6) {{ width: 9%; text-align: center; }}
  td:nth-child(7) {{ width: 7%; text-align: center; }}
  td:nth-child(8) {{ width: 41%; font-size: 7.5pt; color: #333; }}
  p.source {{ font-size: 7.5pt; color: #666; margin: 0 0 6px; }}
  tr.margay-dep td {{ border-left: 3px solid #0066cc; border-right: 3px solid #0066cc; }}
  tr.margay-dep td:first-child {{ border-left: 5px solid #0066cc; }}
  tr.margay-dep td:last-child {{ border-right: 5px solid #0066cc; }}
  p.legend {{ font-size: 7.5pt; color: #333; margin: 2px 0 8px; }}
</style>
</head>
<body>
<h1>NorthernWidget Library Manager Readiness Audit</h1>
<p class="source">Source: {csv_path.name}</p>
<p class="legend">&#9646; Blue border = Margay dependency</p>
{"".join(section_html)}
</body>
</html>"""

html_path = csv_path.with_name(stem + "_icons.html")
html_path.write_text(html, encoding="utf-8")

cmd = [
    "google-chrome", "--headless", "--disable-gpu",
    "--no-sandbox", "--disable-dev-shm-usage",
    f"--print-to-pdf={pdf_path}",
    "--print-to-pdf-no-header",
    str(html_path),
]
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0:
    print(f"PDF written:      {pdf_path}")
    html_path.unlink()   # clean up intermediate HTML
else:
    print("Chrome error:"); print(result.stderr)
    print(f"HTML left at:     {html_path}")
