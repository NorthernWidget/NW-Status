# NW-Status

At-a-glance status of every NorthernWidget hardware design and firmware/software library across the current threads of work: bringing the libraries to a common form, the Schema 1 (NW-Device-Specification) rollout, and hardware readiness.

## Use

```
python3 nw_status.py           # scan the workspace and GitHub, then render
python3 nw_status.py scan      # write nw_status_<date>.csv only
python3 nw_status.py render    # render the latest dated CSV to .md and _icons.pdf
```

The NW repositories are expected in the parent directory of this one, or in `$NW_WORKSPACE` if set. Rendering the PDF needs Google Chrome; without it the Markdown and the intermediate HTML are still produced. GitHub queries use the `gh` CLI.

## What is scanned and what is hand-maintained

Almost every cell is derived from the working tree, git, the GitHub API, or the NW-Device-Specification text at scan time: required files, `library.properties` fields, tags, `begin()` return type, the common-API facets (including casing in two steps: camelCase conversion, then PascalCase removed), open and bug-labelled issues, uncommitted and unpushed state, design-file formats.

Cells that no scanner can read live in `nw_status_manual.csv` as `Row,Column,Value` and are merged over the scanned values: Schema 1 firmware and library state, hardware verification, next actions, notes. Edit that file when a hand-tracked state changes; rerun the scan for everything else.

## Outputs

- `nw_status_<date>.csv` — one row per device (its library and hardware repo side by side) or per unpaired library; one fact or one check per column.
- `nw_status_<date>.md` — one table per thread of work, rows banded as Devices / Standalone libraries / Bare repos; a column in which every row passes or does not apply is hidden and listed under the table.
- `nw_status_<date>_icons.pdf` — the master table with every column, group bands over the columns, one icon per cell (not committed; regenerate).

Dated CSV and Markdown snapshots are committed so that the state on a given day can be recovered.

## Archive

`archive/` holds the May 2026 Library Manager readiness audits and their render script, which this tool supersedes.
