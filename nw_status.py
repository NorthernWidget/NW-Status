#!/usr/bin/env python3
"""
NorthernWidget status table: scan repos + GitHub, write CSV, render Markdown.

  python3 nw_status.py scan      # -> nw_status_<today>.csv (auto columns + manual overrides)
  python3 nw_status.py render    # latest dated CSV -> README.md (between markers) + _icons.pdf
  python3 nw_status.py           # both

The NW repositories are expected in the parent directory of this one, or in
$NW_WORKSPACE if set.

Manual cells (things no scanner can read: Schema 1 firmware state, next
actions, hardware verification) live in nw_status_manual.csv as
  Row,Column,Value
and are merged over the scanned values.  Every other cell is derived from the
working tree, git, or the GitHub API at scan time; the CSV records the scan date.

Successor to archive/nw_library_audit_render.py and the May 2026 audits.
"""
import base64
import csv
import subprocess
import json, datetime, json, re, subprocess, sys, urllib.request
from pathlib import Path

import os
HERE  = Path(__file__).resolve().parent                       # this repo: script, manual CSV, outputs
ROOT  = Path(os.environ.get("NW_WORKSPACE", HERE.parent))     # workspace holding the NW repos
TODAY = datetime.date.today().isoformat()
MANUAL = HERE / "nw_status_manual.csv"
SPEC_README = ROOT / "NW-Device-Specification" / "README.md"

# ── inventory ─────────────────────────────────────────────────────────────────
# (local dir, type, paired device or "")   type: Sensor | Logger | Component
LIBRARIES = [
    ("Apis_Library",        "Sensor",    "Apis"),
    ("Haar_Library",        "Sensor",    "Haar"),
    ("Walrus_Library",      "Sensor",    "Walrus"),
    ("Libelle_Library",     "Sensor",    "Libelle"),
    ("Liasis_Library",      "Sensor",    "Liasis"),
    ("Margay_Library",      "Logger",    "Margay"),
    ("Okapi_Library",       "Logger",    "Okapi"),
    ("MCP3421",             "Component", ""),
    ("NW_BME280",           "Sensor",    ""),
    ("DS3231",              "Component", ""),
    ("DS3231_Logger",       "Component", ""),
    ("MaxBotix_Library",    "Sensor",    ""),
    ("T9602_Library",       "Sensor",    ""),
    ("Tally_Library",       "Sensor",    "Tally"),
    ("TP-Downhole_Library", "Sensor",    ""),
    ("MS5803",              "Component", ""),
    ("VEML6030",            "Component", ""),
    ("VEML6075",            "Component", ""),
    ("TCA9534",             "Component", ""),
    ("MCP23018",            "Component", ""),
    ("MCP4725",             "Component", ""),
]
HARDWARE = [  # (local dir, device)
    ("Project-Apis",    "Apis"),
    ("Project-Haar",    "Haar"),
    ("Project-Walrus",  "Walrus"),
    ("Project-Libelle", "Libelle"),
    ("Project-Liasis",  "Liasis"),
    ("Project-Margay",  "Margay"),
    ("Project-Okapi",   "Okapi"),
    ("Project-Tally",   "Tally"),
]

LIB_COLS = ["Library", "Type", "Device", "GitHub", "version=", "Last tag", "version = tag",
            "library.properties", "paragraph=", "url= ok", "category=", "depends=",
            "LICENSE", "README DOI badge", "CITATION.cff", ".zenodo.json", "keywords.txt",
            "doxygen_NW.cfg", "src/", "_Demo example", "Examples", "docs.yml",
            "moxygen remnants", ".doxybook config", "README API link",
            "begin() -> bool", "getHeader/getString", "Raw-readings triad",
            "camelCase conversion", "PascalCase removed",
            "Header trailing space", "Header separator", "Arduino registry",
            "Schema 1: library", "Open issues", "Uncommitted files", "Unpushed commits",
            "Next action", "Notes"]
HW_COLS  = ["Device", "Repo", "GitHub", "Last tag", "Commits past tag", "Eagle .brd", "KiCad .kicad_pcb",
            "KiCad verified vs Eagle", "Spec appendix", "Schema 1: firmware",
            "Page 0 provisioned + tested", "Open issues", "Bug-labelled issues",
            "Website API link", "Website links = repos", "Website I2C address",
            "Uncommitted files", "Unpushed commits", "Next action", "Notes"]

# Combined table: one row per device (library + hardware) or per unpaired library.
# Library columns keep their names; hardware columns are prefixed "HW: ".
HW_PREFIX = "HW: "
LIB_ONLY = [c for c in LIB_COLS if c not in ("Device", "Next action", "Notes")]
HW_ONLY  = [HW_PREFIX + c for c in HW_COLS if c not in ("Device", "Next action", "Notes")]
COLS = ["Row", "Type"] + [c for c in LIB_ONLY if c != "Type"] + HW_ONLY + ["Next action", "Notes"]

# ── helpers ───────────────────────────────────────────────────────────────────
def sh(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True)
    return r.stdout.strip()

def gh(path, jq):
    out = sh(f"gh api '{path}' --jq '{jq}' 2>/dev/null")
    return out if out else "?"

def slug_of(d):
    url = sh("git remote get-url origin", cwd=d)
    m = re.search(r"github\.com[:/]([^/]+/[^/\s]+?)(?:\.git)?$", url)
    return m.group(1) if m else ""

def props(d):
    p = d / "library.properties"
    if not p.exists():
        return None
    out = {}
    for line in p.read_text(errors="replace").splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out

def headers(d):
    hs = list((d / "src").glob("*.h")) if (d / "src").is_dir() else list(d.glob("*.h"))
    return hs

def read_all(paths):
    return "\n".join(p.read_text(errors="replace") for p in paths)

def public_methods(text):
    """Return list of (name, deprecated?) for method declarations in public: sections."""
    out, pub, dep_pending = [], False, False
    for line in text.splitlines():
        s = line.strip()
        if re.match(r"public\s*:", s): pub = True; continue
        if re.match(r"(private|protected)\s*:", s): pub = False; continue
        if s.startswith("class ") or s.startswith("struct "): pub = False
        if not pub or s.startswith(("//", "*", "/*")): continue
        dep = "[[deprecated" in s or dep_pending
        dep_pending = s.startswith("[[deprecated") and "(" not in s
        m = re.match(r"(?:\[\[deprecated[^\]]*\]\]\s*)?[A-Za-z_][\w:<>*&\s]*?\s[*&]?([A-Za-z_]\w*)\s*\(", s)
        if m and not re.match(r"(if|for|while|switch|return)\b", m.group(1)):
            out.append((m.group(1), dep))
    return out

def begin_types(text):
    out = set()
    for line in text.splitlines():
        s = line.strip()
        if s.startswith(("//", "*", "/*")): continue
        m = re.match(r"(?:virtual\s+|static\s+)?([A-Za-z_][\w:<>]*)\s+begin\s*\(", s)
        if m and not m.group(1).endswith(":"): out.add(m.group(1))
    return sorted(out)

def header_format(d):
    """Return (trailing-space check, separator fact) for the getHeader() string literals."""
    srcs = list((d / "src").glob("*.cpp")) + list(d.glob("*.cpp"))
    text = read_all(srcs) if srcs else ""
    m = re.search(r"String\s+\w+::[gG]etHeader\s*\([^)]*\)\s*\{(.*?)\n\}", text, re.S)
    if not m:
        return "—", "—"
    lits = re.findall(r'"([^"]*)"', m.group(1))
    lits = [l for l in lits if "," in l or "[" in l]
    if not lits:
        return "?", "?"
    trailing = "yes" if any(l.endswith(" ") for l in lits) else "OK"
    sep = "comma-space" if any(", " in l for l in lits) else "comma"
    return trailing, sep

def git_state(d):
    tag   = sh("git describe --tags --abbrev=0 2>/dev/null", cwd=d) or "none"
    dirty = sh("git status --porcelain | wc -l", cwd=d)
    ahead = sh("git rev-list --count @{u}..HEAD 2>/dev/null", cwd=d) or "?"
    past  = sh(f"git rev-list --count {tag}..HEAD 2>/dev/null", cwd=d) if tag != "none" else "?"
    return tag, dirty, ahead, past

def registry():
    try:
        txt = urllib.request.urlopen(
            "https://raw.githubusercontent.com/arduino/library-registry/main/repositories.txt",
            timeout=20).read().decode()
        return set(l.strip().lower().rstrip("/").removesuffix(".git") for l in txt.splitlines())
    except Exception as e:
        print(f"registry fetch failed: {e}", file=sys.stderr)
        return None

_WEBSITE = {}
def website_section(device):
    """The device's '## Device' section on docs.northernwidget.com (sensors.md / loggers.md), or None."""
    if not _WEBSITE:
        for page in ("sensors", "loggers"):
            try:
                b64 = subprocess.run(["gh", "api", f"repos/NorthernWidget/NorthernWidget.github.io/contents/_pages/{page}.md",
                                      "-q", ".content"], capture_output=True, text=True, timeout=30).stdout
                _WEBSITE[page] = base64.b64decode(b64).decode(errors="replace")
            except Exception as e:
                print(f"website fetch failed ({page}): {e}", file=sys.stderr); _WEBSITE[page] = ""
    for txt in _WEBSITE.values():
        m = re.search(rf"^## {re.escape(device)}\s*$(.*?)(?=^#|\Z)", txt, re.M | re.S)
        if m: return m.group(1)
    return None

def website_address(device):
    """Address the website's I2C reference table lists for the device, or None."""
    for txt in _WEBSITE.values():
        m = re.search(rf"^\| \[{re.escape(device)}\]\([^)]*\) \| `(0x[0-9A-Fa-f]+)`", txt, re.M)
        if m: return m.group(1)
    return None

def spec_address(device):
    """(type, Schema 1 address text) from the spec's address registry row, or (None, None) if absent."""
    if not SPEC_README.exists(): return (None, None)
    txt = SPEC_README.read_text()
    i = txt.find("| Device | Type | Current address(es) |")          # the address registry table only
    if i < 0: return (None, None)
    txt = txt[i:txt.find("\n\n", i) if txt.find("\n\n", i) > 0 else len(txt)]
    m = re.search(rf"^\| {re.escape(device)} \| ([^|]*) \| [^|]* \| ([^|]*) \|", txt, re.M)
    if not m: return (None, None)
    a = re.search(r"0x[0-9A-Fa-f]+", m.group(2))
    return (m.group(1).strip(), a.group(0) if a else m.group(2).strip().strip("`"))

def spec_appendix(device):
    if not SPEC_README.exists(): return "?"
    txt = SPEC_README.read_text()
    return "yes" if re.search(rf"^### {device}\b", txt, re.M) else "no"

def load_manual():
    m = {}
    if MANUAL.exists():
        for r in csv.DictReader(open(MANUAL, newline="")):
            m[(r["Row"], r["Column"])] = r["Value"]
    return m

# ── scan ──────────────────────────────────────────────────────────────────────
def scan_library(dirname, typ, device, reg):
    d = ROOT / dirname
    row = {c: "" for c in LIB_COLS}
    row.update(Library=dirname, Type=typ, Device=device)
    if not d.is_dir():
        row["Notes"] = "not cloned locally"; return row
    slug = slug_of(d); row["GitHub"] = slug
    pr = props(d)
    tag, dirty, ahead, past = git_state(d)
    row["Last tag"] = tag
    row["Uncommitted files"] = dirty; row["Unpushed commits"] = ahead
    if pr is None:
        row["library.properties"] = "MISSING"
    else:
        row["library.properties"] = "OK"
        row["version="] = pr.get("version", "")
        row["version = tag"] = ("yes" if tag != "none" and tag.lstrip("v") == pr.get("version") else
                                "no tag" if tag == "none" else f"NO ({tag} vs {pr.get('version')})")
        row["paragraph="] = "OK" if pr.get("paragraph") else "blank"
        url = pr.get("url", "")
        row["url= ok"] = ("OK" if slug and slug.lower() in url.lower()
                          else ("blank" if not url else f"WRONG ({url.split('github.com/')[-1]})"))
        row["category="] = pr.get("category") or "MISSING"
        row["depends="] = pr.get("depends", "")
    row["LICENSE"]        = "OK" if (d / "LICENSE").exists() else "MISSING"
    rd = d / "README.md"
    row["README DOI badge"] = ("MISSING README" if not rd.exists() else
                               "concept DOI" if "zenodo.org/badge/DOI/10.5281" in rd.read_text(errors="replace") else
                               "latestdoi (deprecated)" if "latestdoi" in rd.read_text(errors="replace") else "no badge")
    row["CITATION.cff"]   = "OK" if (d / "CITATION.cff").exists() else "MISSING"
    row[".zenodo.json"]   = "OK" if (d / ".zenodo.json").exists() else "MISSING"
    row["keywords.txt"]   = "OK" if (d / "keywords.txt").exists() else "MISSING"
    dox = list(d.glob("doxygen*.cfg"))
    row["doxygen_NW.cfg"] = ("OK" if (d / "doxygen_NW.cfg").exists() else
                             f"named {dox[0].name}" if dox else "MISSING")
    row["src/"]           = "OK" if (d / "src").is_dir() else "flat layout"
    ex = d / "examples"
    exs = sorted(p.name for p in ex.iterdir() if p.is_dir()) if ex.is_dir() else []
    demo = [e for e in exs if e.endswith("_Demo")]
    row["_Demo example"]  = demo[0] if demo else "MISSING"
    row["Examples"]       = ", ".join(exs) if exs else "none"
    row["docs.yml"]       = "OK" if (d / ".github/workflows/docs.yml").exists() else "MISSING"
    rem = [n for n in ("build_docs.sh", "library_reference.md", ".README-intro.md", "README-intro.md") if (d / n).exists()]
    row["moxygen remnants"] = "OK" if not rem else ", ".join(rem)
    dbc = d / ".doxybook/config.json"
    if not dbc.exists(): row[".doxybook config"] = "MISSING"
    else:
        try: base = json.loads(dbc.read_text()).get("baseUrl", "")
        except Exception: base = "unparseable"
        row[".doxybook config"] = "OK" if base == f"/{dirname}/" else f"baseUrl WRONG ({base})"
    row["README API link"] = ("MISSING README" if not rd.exists() else
                              "OK" if re.search(rf"(docs\.northernwidget\.com|northernwidget\.github\.io)/{re.escape(dirname)}/",
                                                rd.read_text(errors="replace")) else "MISSING")
    hs = headers(d); text = read_all(hs) if hs else ""
    bt = begin_types(text)
    row["begin() -> bool"] = ("no begin()" if not bt else "OK" if bt == ["bool"] else ", ".join(bt))
    has_gh = bool(re.search(r"\b[gG]etHeader\s*\(", text)); has_gs = bool(re.search(r"\b[gG]etString\s*\(", text))
    row["getHeader/getString"] = ("N/A" if typ != "Sensor" and not (has_gh or has_gs) else
                                  "OK" if has_gh and has_gs else "MISSING")
    row["Raw-readings triad"] = ("N/A" if typ != "Sensor" else
                                 "OK" if all(re.search(rf"\b{f}\s*\(", text) for f in
                                             ("beginRawReadings", "takeRawReading", "endRawReadings")) else "MISSING")
    meths = public_methods(text)
    classes = set(re.findall(r"^\s*class\s+(\w+)", text, re.M))
    names = set(n for n, _ in meths)
    upper = [(n, dep) for n, dep in meths if re.match(r"[A-Z][a-z]", n) and n not in classes]
    live_upper = sorted(set(n for n, dep in upper if not dep))
    dep_upper  = sorted(set(n for n, dep in upper if dep))
    # Step 1, camelCase conversion: every PascalCase method has a camelCase twin, and any
    # PascalCase name still present is marked [[deprecated]].
    only_pascal = [n for n in live_upper if (n[0].lower() + n[1:]) not in names]
    unmarked    = [n for n in live_upper if n not in only_pascal]
    def lst(ns): return ", ".join(ns[:4]) + (" …" if len(ns) > 4 else "")
    row["camelCase conversion"] = ("PascalCase only: " + lst(only_pascal) if only_pascal else
                                   "unmarked aliases: " + lst(unmarked) if unmarked else "OK")
    # Step 2, PascalCase removed: no PascalCase public method remains, deprecated or not.
    n_pascal = len(set(live_upper) | set(dep_upper))
    row["PascalCase removed"] = ("OK" if n_pascal == 0 else
                                 f"pending ({len(dep_upper)} deprecated aliases)" if not live_upper else
                                 f"NO ({n_pascal} PascalCase live)")
    row["Header trailing space"], row["Header separator"] = header_format(d) if typ == "Sensor" else ("—", "—")
    row["Arduino registry"] = ("?" if reg is None else
                               "yes" if f"https://github.com/{slug}".lower() in reg else "no")
    row["Open issues"] = gh(f"repos/{slug}", ".open_issues_count") if slug else "?"
    return row

def scan_hardware(dirname, device):
    d = ROOT / dirname
    row = {c: "" for c in HW_COLS}
    row.update(Device=device, Repo=dirname)
    if not d.is_dir():
        row["Notes"] = "not cloned locally"; return row
    slug = slug_of(d); row["GitHub"] = slug
    tag, dirty, ahead, past = git_state(d)
    row["Last tag"] = tag; row["Commits past tag"] = past
    row["Uncommitted files"] = dirty; row["Unpushed commits"] = ahead
    k = len(list(d.rglob("*.kicad_pcb"))); e = len([p for p in d.rglob("*.brd") if ".git" not in p.parts])
    row["Eagle .brd"] = str(e); row["KiCad .kicad_pcb"] = str(k)
    row["Spec appendix"] = spec_appendix(device)
    row["Open issues"] = gh(f"repos/{slug}", ".open_issues_count") if slug else "?"
    row["Bug-labelled issues"] = gh(f"repos/{slug}/issues?labels=bug&state=open&per_page=100", "length") if slug else "?"
    sec = website_section(device)
    libdir = next((l[0] for l in LIBRARIES if l[2] == device), None)
    libslug = slug_of(ROOT / libdir) if libdir and (ROOT / libdir).is_dir() else None
    if sec is None:
        row["Website API link"] = row["Website links = repos"] = "no entry"
    else:
        row["Website API link"] = ("OK" if libdir and re.search(
            rf"(docs\.northernwidget\.com|northernwidget\.github\.io)/{re.escape(libdir)}/", sec) else "MISSING")
        links = set(m.lower() for m in re.findall(r"github\.com/([\w.-]+/[\w.-]+)", sec))
        want = set(x.lower() for x in (slug, libslug) if x)
        stale = sorted(l for l in links if l not in want)
        row["Website links = repos"] = "OK" if not stale else "stale: " + ", ".join(l.split("/")[0] + "/…" for l in stale)
    site, (styp, spec) = website_address(device), spec_address(device)
    row["Website I2C address"] = ("—" if styp and styp.startswith("Controller") else   # controllers are not on the site's table
                                  "not listed" if site is None else
                                  "OK" if site == spec else
                                  f"{site} (not in spec)" if spec is None else f"{site} (spec {spec})")
    return row

def scan():
    reg = registry()
    manual = load_manual()
    libs = [scan_library(*l, reg) for l in LIBRARIES]
    hws  = [scan_hardware(*h) for h in HARDWARE]
    for rows in (libs, hws):
        for r in rows:
            key = r.get("Library") or r.get("Repo")
            for (rk, col), val in manual.items():
                if rk == key and col in r:
                    r[col] = val
    unknown = [(rk, col) for (rk, col) in manual
               if rk not in [r["Library"] for r in libs] + [r["Repo"] for r in hws]
               or col not in LIB_COLS + HW_COLS]
    if unknown:
        print(f"WARNING: manual entries not applied: {unknown}", file=sys.stderr)
    hw_by_dev = {h["Device"]: h for h in hws}
    combined = []
    for l in libs:
        r = {c: "" for c in COLS}
        r["Row"] = l["Device"] or l["Library"]; r["Type"] = l["Type"]
        for c in LIB_ONLY:
            if c in r: r[c] = l[c]
        h = hw_by_dev.pop(l["Device"], None) if l["Device"] else None
        if h:
            for c in HW_COLS:
                if HW_PREFIX + c in r: r[HW_PREFIX + c] = h[c]
        else:
            for c in HW_ONLY: r[c] = "—"
        r["Next action"] = " · ".join(x for x in ((h or {}).get("Next action", ""), l["Next action"]) if x)
        r["Notes"] = " · ".join(x for x in (l["Notes"], (h or {}).get("Notes", "")) if x)
        combined.append(r)
    for dev, h in hw_by_dev.items():  # hardware with no library row
        r = {c: "" for c in COLS}; r["Row"] = dev; r["Type"] = "Hardware only"
        for c in HW_COLS:
            if HW_PREFIX + c in r: r[HW_PREFIX + c] = h[c]
        r["Next action"], r["Notes"] = h["Next action"], h["Notes"]
        combined.append(r)
    out = HERE / f"nw_status_{TODAY}.csv"
    with open(out, "w", newline="") as f:
        f.write(f"# nw_status scan {TODAY}\n")
        w = csv.DictWriter(f, COLS); w.writeheader(); w.writerows(combined)
    print(f"CSV written: {out}")
    return out

# ── render ────────────────────────────────────────────────────────────────────
GOOD = {"OK", "yes", "concept DOI"}
PASS_THROUGH = ("Row", "Library", "Type", "Device", "GitHub", "Repo", "version=", "Last tag", "depends=",
                "Open issues", "Bug-labelled issues", "Next action", "Notes", "Commits past tag",
                "Eagle .brd", "KiCad .kicad_pcb", "Examples", "Header separator", "Band")
ZERO_IS_GOOD = ("Uncommitted files", "Unpushed commits")

def icon(col, v):
    v = v.strip(); col = col.removeprefix(HW_PREFIX)
    if col in PASS_THROUGH: return v
    if col in ZERO_IS_GOOD: return "✅" if v == "0" else "—" if v in ("", "—") else "?" if v == "?" else "◐"
    if col == "Header trailing space" and v == "yes": return "❌"
    if col == "category=": return "❌" if v == "MISSING" else "✅"
    if col == "moxygen remnants": return "✅" if v == "OK" else "❌"
    if col == "Website I2C address" and v not in ("OK", "—", "?"): return "❌"
    if v == "?": return "?"
    if v in ("", "—", "none") or v.startswith(("N/A", "no begin()")): return "—"
    if v in GOOD or v.startswith("OK") or v.endswith("_Demo"): return "✅"
    if v.startswith(("MISSING", "NO", "no ", "no", "PascalCase", "blank", "WRONG", "latestdoi", "flat", "stale", "baseUrl")): return "❌"
    return "◐"

def read_csv(path):
    lines = [l for l in path.read_text().splitlines() if l.strip() and not l.startswith("#")]
    return list(csv.DictReader(lines))

# Derived (collapsed) cells, computed from the scanned columns at render time.
def derive(r):
    r = dict(r)
    if r.get(HW_PREFIX + "Repo", "—") != "—":                       r["Band"] = "Devices"
    elif r.get("library.properties") == "MISSING":                  r["Band"] = "Bare repos"
    else:                                                           r["Band"] = "Standalone libraries"
    return r

# Column groups: (group title, [columns]).  Order is the master-table order.
GROUPS = [
    ("Directory",        ["Row", "Type", "Library", "GitHub", HW_PREFIX + "Repo", HW_PREFIX + "GitHub",
                          "Arduino registry"]),
    ("Release state",    ["version=", "Last tag", "version = tag", HW_PREFIX + "Last tag", HW_PREFIX + "Commits past tag"]),
    ("Library metadata", ["library.properties", "paragraph=", "url= ok", "category="]),
    ("Release files",    ["LICENSE", "README DOI badge", "CITATION.cff", ".zenodo.json", "keywords.txt",
                          "doxygen_NW.cfg", "src/", "_Demo example", "Examples"]),
    ("Docs conversion",  ["docs.yml", ".doxybook config", "moxygen remnants", "README API link",
                          HW_PREFIX + "Website API link", HW_PREFIX + "Website links = repos",
                          HW_PREFIX + "Website I2C address"]),
    ("Common API: signatures", ["begin() -> bool", "getHeader/getString", "Raw-readings triad"]),
    ("Common API: style",      ["camelCase conversion", "PascalCase removed", "Header trailing space", "Header separator"]),
    ("Schema 1 pipeline", [HW_PREFIX + "Spec appendix", HW_PREFIX + "Schema 1: firmware", "Schema 1: library",
                           HW_PREFIX + "Page 0 provisioned + tested"]),
    ("Hardware design",  [HW_PREFIX + "Eagle .brd", HW_PREFIX + "KiCad .kicad_pcb", HW_PREFIX + "KiCad verified vs Eagle",
                          HW_PREFIX + "Bug-labelled issues"]),
    ("Activity",         ["Open issues", "Uncommitted files", "Unpushed commits",
                          HW_PREFIX + "Open issues", HW_PREFIX + "Uncommitted files", HW_PREFIX + "Unpushed commits"]),
    ("Plan",             ["Next action", "Notes"]),
]
# Per-thread views for the Markdown file: (title, [group titles or column names], band filter or None)
VIEWS = [
    ("Where is everything",   ["Directory", "Activity"], None),
    ("Release readiness (Schema 0 checklist)", ["Release state", "Library metadata", "Release files"], None),
    ("Common sensor API",     ["Common API: signatures", "Common API: style"], None),
    ("Docs conversion (moxygen -> Doxygen on Pages; website entries)", ["Docs conversion"], None),
    ("Schema 1 rollout",      ["Schema 1 pipeline"], "Devices"),
    ("Hardware design",       [HW_PREFIX + "Last tag", HW_PREFIX + "Commits past tag", "Hardware design"], "Devices"),
    ("Next actions",          ["Plan"], None),
]
BAND_ORDER = ["Devices", "Standalone libraries", "Bare repos"]

def expand(items):
    cols = []
    for it in items:
        g = dict(GROUPS).get(it)
        cols += g if g else [it]
    return cols

def all_green(rows, col):
    return all(icon(col, r.get(col, "")) in ("✅", "—") for r in rows)

def short(col):  # header label
    return col.removeprefix(HW_PREFIX) if col.startswith(HW_PREFIX) else col

def cell_md(col, v):
    ic = icon(col, v)
    if ic == v or ic == "?": return v.replace("|", "\\|")
    if ic == "—": return "—"
    if v.strip() in GOOD or v.strip() == "OK" or v.endswith("_Demo") and ic == "✅": return ic
    return f"{ic} {v}".replace("|", "\\|")

def md_view(rows, cols, band_filter=None):
    rows = [r for r in rows if band_filter is None or r["Band"] == band_filter]
    hidden = [c for c in cols if c != "Row" and all_green(rows, c)]
    cols = [c for c in cols if c not in hidden]
    out = ["| " + " | ".join(("HW: " if c.startswith(HW_PREFIX) else "") + short(c) for c in cols) + " |",
           "|" + "---|" * len(cols)]
    for band in BAND_ORDER:
        br = [r for r in rows if r["Band"] == band]
        if not br: continue
        if band_filter is None:
            out.append(f"| **{band}** |" + " |" * (len(cols) - 1))
        for r in br:
            out.append("| " + " | ".join(cell_md(c, r.get(c, "")) if c != "Row" else f"**{r['Row']}**"
                                        for c in cols) + " |")
    if hidden:
        out += ["", "All rows pass or not applicable (column hidden): " +
                ", ".join(f"`{('HW: ' if c.startswith(HW_PREFIX) else '') + short(c)}`" for c in hidden)]
    return "\n".join(out)

INTRO = """## Status — {date}

Generated by `nw_status.py` from the working tree, git, the GitHub API, and NW-Device-Specification. Cells listed in `nw_status_manual.csv` are hand-maintained (Schema 1 firmware and library state, hardware verification, next actions, notes); everything else is scanned. Supersedes `nw_library_audit_2026-05-15.csv`.

One row per device (its library and its hardware repo together) or per unpaired library; rows are banded as **Devices**, **Standalone libraries**, and **Bare repos**. This file carries one table per thread of work; the master table with every column side by side is `nw_status_{date}_icons.pdf`. A column in which every row passes or does not apply is hidden and listed under the table.

Legend: ✅ done · ◐ partial · ❌ missing or wrong · — not applicable · ? not determined

**Common sensor API**: goal is that every sensor library presents the same C++ interface in Arduino style. Facets, one column each: `begin()` returns bool; `getHeader()`/`getString()`; the raw-readings triad `beginRawReadings()`/`takeRawReading()`/`endRawReadings()`; casing in two steps, **camelCase conversion** (every method has a camelCase name and any PascalCase name still present is marked `[[deprecated]]`) then **PascalCase removed** (no PascalCase method remains; "pending" while deprecated aliases are still carried); header string has no trailing space; header separator (`comma` or `comma-space`, a fact rather than a check, since the target format is undecided). Whether every sensor must carry the raw triad is also an open decision.

**Release readiness**: columns follow RELEASING.md, one per required file or field.

Open items that are not per-row: spec appendices still print `Magic=0x00` (spec body says 0x4E); `NorthernWidget_Core` and the `NorthernWidget` bundle library have no repo yet; Firmware-Aggregator `repolist.txt` still names `BME_Library` and `MCP3421`; Symbiont-LiDAR_Library is not cloned locally (superseded by Apis); Monarch/Dyson libraries are archived, split into Libelle and Liasis.
"""

def render(path):
    rows = [derive(r) for r in read_csv(path)]
    date = path.stem.replace("nw_status_", "")
    md = [INTRO.format(date=date)]
    for title, items, band in VIEWS:
        cols = ["Row"] + [c for c in expand(items) if c != "Row"]
        md += [f"### {title}", "", md_view(rows, cols, band), ""]
    # The report lives in README.md between two markers, so the repository page opens on it.
    readme = HERE / "README.md"
    START, END = "<!-- nw_status:begin -->", "<!-- nw_status:end -->"
    text = readme.read_text() if readme.exists() else ""
    body = "\n".join(md).strip("\n")
    if START in text and END in text:
        pre, rest = text.split(START, 1); _, post = rest.split(END, 1)
        text = f"{pre}{START}\n{body}\n{END}{post}"
    else:
        text = text.rstrip("\n") + f"\n\n{START}\n{body}\n{END}\n"
    readme.write_text(text); print(f"Report written into: {readme}")

    # master table: HTML with group bands, row bands, hidden all-green columns -> PDF
    groups = []
    hidden = []
    for title, cols in GROUPS:
        keep = [c for c in cols if c == "Row" or not all_green(rows, c)]
        hidden += [c for c in cols if c not in keep]
        if keep: groups.append((title, keep))
    allcols = [c for _, cols in groups for c in cols]
    band_row = "".join(f'<th class="band" colspan="{len(cols)}">{t}</th>' for t, cols in groups)
    head_row = "".join(f'<th class="col">{("HW: " if c.startswith(HW_PREFIX) else "") + short(c)}</th>' for c in allcols)
    body = ""
    for band in BAND_ORDER:
        br = [r for r in rows if r["Band"] == band]
        if not br: continue
        body += f'<tr><td class="rowband" colspan="{len(allcols)}">{band}</td></tr>'
        for r in br:
            body += "<tr>" + "".join(
                f'<td title="{r.get(c, "")}">{icon(c, r.get(c, ""))}</td>' for c in allcols) + "</tr>"
    hidden_note = ("All rows pass or not applicable (hidden): " +
                   ", ".join(("HW: " if c.startswith(HW_PREFIX) else "") + short(c) for c in hidden)) if hidden else ""
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>NW status {date}</title>
<style>@page{{size:A3 landscape;margin:1cm}} body{{font-family:Arial,sans-serif;font-size:8pt}}
table{{border-collapse:collapse}} th,td{{border:1px solid #aaa;padding:2px 4px;text-align:center;vertical-align:middle}}
th.band{{background:#343a40;color:#fff;font-size:8pt;border-left:2px solid #fff;border-right:2px solid #fff}}
th.col{{background:#6c757d;color:#fff;font-size:7pt;writing-mode:vertical-rl;transform:rotate(180deg);height:110px}}
td.rowband{{background:#e9ecef;text-align:left;font-weight:bold}}
td:first-child{{text-align:left;font-weight:bold}} p.note{{font-size:7.5pt;color:#444}}</style></head><body>
<h1>NorthernWidget status {date}</h1>
<p class="note">Hover a cell for the scanned value. ✅ done · ◐ partial · ❌ missing or wrong · — n/a · ? undetermined</p>
<table><thead><tr>{band_row}</tr><tr>{head_row}</tr></thead><tbody>{body}</tbody></table>
<p class="note">{hidden_note}</p></body></html>"""
    hp = path.with_name(path.stem + "_icons.html"); hp.write_text(html); print(f"HTML written:     {hp}")
    chrome = next((c for c in ("google-chrome", "chromium", "chromium-browser") if sh(f"command -v {c}")), None)
    if chrome:
        pdf = path.with_name(path.stem + "_icons.pdf")
        r = subprocess.run([chrome, "--headless", "--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage",
                            f"--print-to-pdf={pdf}", "--print-to-pdf-no-header", str(hp)], capture_output=True, text=True)
        print(f"PDF written:      {pdf}" if r.returncode == 0 else f"chrome failed: {r.stderr[-300:]}")
        if r.returncode == 0: hp.unlink()

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "both"
    if mode in ("scan", "both"):
        p = scan()
    if mode in ("render", "both"):
        if mode == "render":
            cands = sorted(HERE.glob("nw_status_20[0-9][0-9]-[0-9][0-9]-[0-9][0-9].csv"), reverse=True)
            if not cands: sys.exit("no nw_status_*.csv found")
            p = cands[0]
        render(p)
