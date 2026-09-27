# NW-Status

The cross-cutting state of the Northern Widget workspace: a generated status table over every repository, and `QUEUE.md`, the desk queue of decided-but-unstarted work. This is where a session looks first and writes last.

## Standards

Follow the NW standards in the root `CLAUDE.md` one level above `github/`. Prose here is read by people and is written in Andy's voice at the first draft.

## Working rules

- The table in `README.md` is **generated**: `python3 nw_status.py` rewrites it between the `nw_status:begin/end` markers. Never hand-edit between those markers.
- Hand-tracked facts live in `nw_status_manual.csv` as Row,Column,Value. That file is the place for judgement; the scanner is the place for what can be measured.
- One value per table cell. Width is handled with column groups, never by collapsing two facts into one cell.
- `QUEUE.md` holds work that is decided or open but not started, one line per item, with what blocks it. An item Andy has not reached is **pending, not declined**.
- A finding recorded here as fact must be verified. A superseded finding is corrected in place and marked as superseded rather than deleted: this file has carried a wrong conclusion before, and the correction is as valuable as the finding.

## Hard rule

**Never** create a git tag, GitHub release, or push to a shared remote unless explicitly asked in the current message. If in doubt, ask.
