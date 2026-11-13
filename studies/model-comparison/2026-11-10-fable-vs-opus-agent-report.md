# Fable 5.1 vs Opus: retrospective comparison from the record

**Status: COMPLETE** (2026-11-10)


**Lead.** Fable 5.1 bundles more changes per commit (blinded: 28.9 % of 45 judged MULTI against 11.1 % for Opus 5 and 6.7 % for Opus 5.5, in both overlapping months) and held a repeated reporting instruction far less well (4 of 47 against 63 of 71 after the same request). Opus 5.5 reports check counts in its messages far more often. Rework, reverts and Andy's correction rate do not separate the models once era is accounted for: corrections fall with the calendar (10.8, 6.1, 3.3 per 100 assistant turns for Opus 5, Fable, Opus 5.5). The full summary is in "What the measures show" below, followed by the limits and the head-to-head design.

Judge: this analysis is run by an Opus model (Opus 5.5) judging Opus against Fable. Qualitative judgments were blinded (see Method).

## Sources log

Scripts live in the scratch area `/tmp/claude-1000/-home-awickert-Dropbox-NorthernWidget-github/cf0342fa-36e3-4818-be1e-2b4b31cc1756/scratchpad/` (copied beside this report at the end as `scripts/`).

- `g_inventory.py`: every commit (all refs) in every git repository directly under the workspace plus `~/misc/claude-kicad-text` and `~/misc/wickert-voice` whose message carries `Co-Authored-By: Claude <family> <version>`. Output `commits.csv`. Result: 2,466 trailered (repo, sha) rows; by model and month: Fable 5.1 2026-09 658, 2026-10 117, 2026-11 429; Opus 4.8 2026-08 4; Opus 5 2026-09 192, 2026-10 318; Opus 5.5 2026-11 261; Sonnet 4.6 475 (May-June); Sonnet 5.5 12. Sonnet and Opus 4.8 are excluded below.
- `t_inventory.py`, `t_timeline.py`: transcripts in `~/.claude/projects/-home-awickert-Dropbox-NorthernWidget-github*`. Only three main-thread sessions carry real work: `30dafa30` (Opus 5, 2026-09-23 to 10-19; Fable 5.1, 10-20 to 10-22), `cf0342fa` (Fable 5.1, 10-20 to 11-06; Opus 5.5, 11-06 to 11-10; Sonnet 5.5, 181 messages on 11-06), plus subagent files. The 21 sibling per-repository project directories hold 12-72 kB each (no Claude 5-era sessions of substance).
- Dead end: the Fable 5.1 sessions of 2026-09-20 to 09-23 that produced 653 commits have no transcript in any NW project directory (a grep for `claude-fable-5-1` across all of `~/.claude/projects` finds Fable transcripts only from 2026-09-18 onward in unrelated projects, and none in NW before 10-20). Transcript measures therefore cover Fable only from 10-20.

### The era structure (the main confound)

Commit days by model (from `commits.csv`, author dates): Fable 2026-09-20 to 09-24 (658 commits); Opus 5 2026-09-24 to 10-20 (510); Fable 10-20 to 11-06 (546); Opus 5.5 11-04 to 11-10 (261). Days with both: 09-24 (Opus 86, Fable 5), 10-20 (Fable 36, Opus 8), 11-04 (Opus 39, Fable 78), 11-06 (Opus 37, Fable 9). The eras alternate F-O-F-O, which lets an era-adjacent comparison stand in, weakly, for an overlap comparison; true same-day overlap is small.

## Confirmed results (appended as obtained)

Kinds are assigned per commit by `common.py: kind()`: sim/tests = NW-Sim, NW-Tests, NW-Provision, NW-Build, claude-kicad-text; docs/status = NW-Status, NW-Device-Specification, NW-Registry, wickert-voice, Inclinometer-Selection, Deployments; hardware = nw-cold-silicon, or any commit whose KiCad/Eagle files are at least as many as its firmware files, or a Project-* commit with neither; firmware = everything else. Repositories named `*.backup` or `*Archive*` are excluded and shas are deduplicated, which leaves Fable 5.1 1,204, Opus 5 510 and Opus 5.5 261 commits.

### R1. Process compliance from git (`m_compliance.py`, `a_compliance.py`, `a_compliance2.py`; all 1,975 commits)

Words below are "clean" words: commit message without trailers, plus added lines of .md/.txt/.tex/.rst/.cff files that are not under `corpus/` or `reports/`, not in a file receiving more than 1,500 lines, not a Markdown table row, and not longer than 600 characters, plus added lines of code files. These exclusions are mine and were needed because Andy's own 567,409-word corpus import and generated status tables (an em-dash for an empty cell) otherwise dominate.

| model | commits | median files/commit | % commits >5 files | % with Claude-Session trailer | % with a test/check count in the message |
|---|---|---|---|---|---|
| Fable 5.1 | 1,204 | 1 | 6.8 | 100.0 | 3.2 |
| Opus 5 | 510 | 1 | 3.5 | 98.6 | 4.3 |
| Opus 5.5 | 261 | 1 | 2.3 | 98.1 | 23.8 |

Like with like (kind x month, n in parentheses): docs/status 2026-09, Fable (186) 2.2 % >5 files vs Opus 5 (73) 0.0 %; firmware 2026-09 Fable (361) 6.6 % vs Opus 5 (46) 2.2 %; sim/tests 2026-09 Fable (50) 10.0 % vs Opus 5 (71) 4.2 %; hardware 2026-11 Fable (267) 13.1 % vs Opus 5.5 (112) 1.8 %; docs/status 2026-11 Fable (114) 0.0 % vs Opus 5.5 (122) 0.8 %. Fable's commits touch more files more often in four of five same-month strata. The test-count difference is concentrated in hardware 2026-11: Opus 5.5 52.7 % (112) against Fable 1.9 % (267); in docs/status 2026-11 it is Fable 3.5 % vs Opus 5.5 0.8 %.

British spellings (`spelling_check.scan`, hard hits only) and em-dashes, per 10,000 clean words, split at 2026-10-27, the day `spelling_check.py` was created:

| model, period | commits | clean words | British /10k | commits with a British form | em-dash /10k (prose + message) |
|---|---|---|---|---|---|
| Fable 5.1, before 10-27 | 722 | 215,474 | 9.33 | 90 | 9.62 |
| Opus 5, before 10-27 | 510 | 248,455 | 9.46 | 122 | 5.37 |
| Fable 5.1, from 10-27 | 482 | 128,970 | 4.03 (3.67 without wickert-voice) | 22 | 0.00 |
| Opus 5.5, from 10-27 | 261 | 89,019 | 0.90 | 2 | 0.12 |

Before the rule the two are equal on spelling; Fable wrote more em-dashes (by month: Fable 2026-09 10.46, Opus 5 2026-09 8.67, Opus 5 2026-10 3.79, Fable 2026-10 1.34). After the rule Fable's British hits fall in 2026-10-27 to 11-03 (18 in 21,599 message words, 10 in prose, 16 in code) and stop; on the overlap days 11-04 to 11-06 both models have zero.

### R2. Reverts and explicit corrections of a named earlier commit (`m_reverts.py`, all refs, all authors)

A commit counts when its message names an earlier Claude commit's hash in the same repository and is a `git revert` or carries a correction word. Fable 5.1: 8 references in 1,204 commits (0.66 per 100), 0 git reverts, every one a later Fable or Opus commit restoring text or comments a Fable commit had dropped (Bobby Schulz's notes, README sections), plus one self-revert of fifteen KiCad stage-6 commits after Fable's own gate caught nets 200 of 209 (Project-Okapi c9581dea). Opus 5: 7 (1.37 per 100), 4 git reverts by Andy: three Project-Apis firmware commits reverted 2026-09-24 after he asked for a datasheet re-check (LiDAR start command, auto-increment bit), and the Project-Walrus MS5803 table reverted 2026-09-30 as "far more complex than it must be". Opus 5.5: 6 (2.30 per 100), 3 git reverts by Andy of one change split in three commits (Okapi R48 moved for #36, reverted 2026-11-10 when he judged the original land pattern better), and two Fable commits on 11-04 correcting Opus 5.5 Margay BoM entries (a manufacturer misspelling and R19 100 kOhm, not 100 Ohm). Counts this small (21 in all) do not separate the models.

### R3. Rework (`r_rework.py`, `a_rework.py`; stratified sample, 60 per model family x kind, spread over months)

477 commits analyzed (Fable 240, Opus 237: Opus 5 135, Opus 5.5 102). Survival = lines the commit added that `git blame` (honoring `.git-blame-ignore-revs`) still attributes to it, at HEAD and at the first HEAD-ancestor 3 days later. Touch = a later HEAD-ancestor commit that deletes or modifies at least one of those lines (blame of its parent over its removed ranges); "fixword" = the touching commit's subject matches fix/correct/revert/wrong/restore. A commit enters a W-day touch rate only if W days have passed, which removes most Opus 5.5 commits from the 7-day rate.

| family | n | HEAD survival, line-weighted | median per commit | 3-day survival lw | 7-day touched | 7-day fix-word touched |
|---|---|---|---|---|---|---|
| Fable 5.1 | 240 | 0.368 | 0.875 | 0.391 (240) | 62.4 % (210) | 1.9 % |
| Opus 5 + 5.5 | 237 | 0.896 | 1.000 | 0.929 (173) | 59.3 % (135) | 8.9 % |

The line-weighted gap is a hardware artifact: Fable hardware 2026-11 (35) survives 0.33 because KiCad re-saves rewrite whole files, and Opus has almost no hardware work before November. Like with like the picture is mixed: docs/status 2026-09, Fable (20) 0.60 lw vs Opus 5 (20) 0.80, 7-day fix-word 10 % vs 15 %; firmware 2026-09 Fable (34) 0.66 vs Opus 5 (21) 0.29, fix-word 0 % vs 9.5 %; sim/tests 2026-09 Fable (22) 0.84 vs Opus 5 (20) 0.88, fix-word 0 % vs 15 %; sim/tests 2026-10 Fable (14) 0.16 vs Opus 5 (21) 0.74 at HEAD but 0.83 vs 0.80 at 3 days. The fix-word rate depends on how the later commit was worded, and Fable's subjects are declarative ("the LTO note was wrong") rather than "Fix ...", which the blinded reading below is meant to correct.

### R4. Objective transcript measures (`t_turns.py`, `t_textstats.py`, `t_summary_after_ask.py`)

Human turns are Andy's typed messages in the main threads of `30dafa30` and `cf0342fa` (tool results, notifications, slash-command echoes and hook injections excluded), each attributed to the model of the reply before it: Opus 5 396, Fable 5.1 361, Opus 5.5 242, Sonnet 5.5 22 (dropped). Reply episodes: Opus 5 383, Fable 355, Opus 5.5 240. Interrupts: 3, 2, 1.

| model | replies | em-dash per 1k words | flattery opener | replies >300 words | ending in the fixed `---` / `**Summary.**` form |
|---|---|---|---|---|---|
| Opus 5 (09-23 to 10-20) | 396 | 13.63 | 2.5 % | 283 | 72.8 % |
| Fable 5.1 (10-20 to 11-06) | 361 | 0.50 | 0.3 % | 165 | 23.0 % |
| Opus 5.5 (11-06 to 11-10) | 242 | 0.00 | 0.4 % | 153 | 78.4 % |

The Summary gap is partly era: on the one shared day, 11-06, Fable ended 1 of 10 long replies in the form and Opus 5.5 2 of 10. The sharper evidence is the response to the same request. Andy asked Fable to resume the standard summaries at 2026-11-04T18:17Z, and asked Opus 5.5 at 11-08T06:47Z (again 11-10T03:57Z). In the 48 hours before each ask the rates were Fable 11/39 and Opus 5.5 2/26; in the 12 hours after, Fable 5/10 and Opus 5.5 12/13; from 12 to 48 hours after, Fable 4/47 and Opus 5.5 63/71. No memory file recorded the rule until 11-10, so the 11-08 compliance was not carried by one. This is one ask per model, which is a case, not a rate.

Correction to R4 counts: the two session files share the 10-20 to 10-22 lines, so 36 human turns appeared twice; `t_turns.py` now deduplicates by uuid. Deduplicated human turns: Opus 5 396, Fable 5.1 325, Opus 5.5 242. Fable's rates change little (325 replies, em-dash 0.57 per 1k words, flattery opener 0.3 %, Summary form 34 of 146 = 23.3 %); the other rows are unchanged.

### R5. Blinded reading of the 7-day touches (`b_touch_blind.py`, judge output `touch_judged.csv`, unblinded by `u_unblind.py`)

A separate Opus judge, given only trailer-stripped and model-scrubbed messages, the lag and the diffstat, labeled 100 touch pairs (50 per family, seeded random from 333 Fable and 191 Opus touches within 7 days): Fable-authored originals FIX 7, SUPERSEDE 42, UNCLEAR 1 (14 % of touches); Opus 5 FIX 9 of 34 (26 %); Opus 5.5 FIX 1 of 16. The subject-line fix-word regex caught only 2 of the 17 judged fixes, which confirms that the regex measure in R3 is not usable. Scaling by touches per sampled commit (Fable 1.39, Opus 5 1.02) gives about 19 fix-touches per 100 Fable commits and 27 per 100 Opus 5 commits, from 7 and 9 judged fixes; the intervals overlap widely. Opus 5.5's 7-day window is mostly unobserved (0.52 touches per commit), so it is not comparable here. The judge classified datasheet-driven part changes inherited from Eagle as SUPERSEDE and dash, voice and terminology rewrites as FIX.

### R6. Andy's corrections in transcripts, blinded (`b_turns_blind.py`, judges `turns_judged_1.csv`, `turns_judged_2.csv`, `u_unblind.py`)

Sample: 120 human turns per model, seeded random, each with the last 700 characters of the reply before it; model names, URLs and dates scrubbed; items ordered by hash and split between two Opus judges who were told not to open the key. After deduplication 354 distinct turns (Fable 114). Classification rule given to the judges: CORRECTION if the turn says or clearly implies the assistant was wrong, overreached, ignored an instruction or standing rule, or must redo or revert work, including a plainer restatement that signals a miss; NOT for new requests, approvals, questions, information, future preferences and neutral steering; UNCLEAR if ambiguous. Each sampled turn follows exactly one reply episode, so the rate per 100 human turns is the rate per 100 assistant turns (episodes and human turns agree within 3 %).

| model (era) | turns judged | CORRECTION | per 100 assistant turns (95 % Wilson) | CORRECTION + UNCLEAR | types |
|---|---|---|---|---|---|
| Opus 5 (09-23 to 10-20) | 120 | 13 | 10.8 (6.4-17.7) | 20.8 (14.5-28.9) | wrong 4, ignored-instruction 4, report-form 3, overreach 1, other 1 |
| Fable 5.1 (10-20 to 11-06) | 114 | 7 | 6.1 (3.0-12.1) | 12.3 (7.5-19.6) | wrong 3, other 2, redo 1, report-form 1 |
| Opus 5.5 (11-06 to 11-10) | 120 | 4 | 3.3 (1.3-8.3) | 8.3 (4.6-14.7) | other 2, wrong 1, report-form 1 |

The ordering follows the calendar (09-10 highest, then 10-11, then 11), not the model family, which is what an era effect (a maturing rule set, a settled project, a calmer user) would produce as readily as a model effect. The eras do not overlap in the transcripts except 11-06, where n is too small to split.

### R7. Commit granularity, blinded (`b_gran_blind.py`, judge output `gran_judged.csv`, `u_gran.py`)

45 commits per model, seeded and round-robin across kinds; the judge saw the scrubbed message, the diffstat and the first 50 diff lines and labeled ONE logical change, MULTI (separable changes bundled) or UNCLEAR, plus message quality 1-3. Fable 5.1: MULTI 13 of 45 (28.9 %), quality 2.38. Opus 5: 5 of 45 (11.1 %), 2.82. Opus 5.5: 3 of 45 (6.7 %), 2.73. Same month: 2026-09 Fable 7 of 25 vs Opus 5 2 of 19; 2026-11 Fable 3 of 15 vs Opus 5.5 3 of 45. Same kind: firmware Fable 5 of 11 vs Opus 5 3 of 14 and Opus 5.5 0 of 8; docs/status Fable 4 of 12 vs Opus 5 2 of 15 and Opus 5.5 3 of 13. The direction holds in both overlapping months and in every kind, and agrees with R1's files-per-commit tail; each cell is small.

## What the measures show

1. **Granularity is the most consistent difference.** Fable 5.1 bundles more: 28.9 % of blinded commits judged MULTI against 11.1 % (Opus 5) and 6.7 % (Opus 5.5), in the same direction within 2026-09 and 2026-11 and in every repository kind, and more commits touching more than five files in four of five same-month strata. Its messages were rated lower (2.38 against 2.82 and 2.73).
2. **Following a repeated instruction.** After the same request to resume the fixed closing summary, Fable complied in 4 of 47 long replies 12-48 hours later; Opus 5.5 in 63 of 71. One ask per model, so a strong case rather than a rate.
3. **Testing evidence in messages.** Opus 5.5 states a check count in 23.8 % of its commits (52.7 % of its November hardware commits) against Fable's 1.9 % on November hardware.
4. **Rework does not separate the models.** Blinded, 14 % of the 7-day touches to Fable commits were fixes against 26 % for Opus 5 (about 19 against 27 fix-touches per 100 commits, from 7 and 9 judged fixes). Explicit corrections naming a commit: 8, 7 and 6 (Fable, Opus 5, Opus 5.5). Andy's own git reverts land on Opus 5 (4) and Opus 5.5 (3, one change), none on Fable; Fable has the one large self-revert, caught by its own gate. Line survival is dominated by KiCad re-saves and is not a quality measure for hardware.
5. **Andy's corrections fall with the calendar, not the model family:** 10.8 (Opus 5, Sep-Oct), 6.1 (Fable, Oct-Nov), 3.3 (Opus 5.5, Nov) per 100 assistant turns; neighboring intervals overlap.
6. **Rule compliance tracks the rule's arrival.** British spellings were equal before the spelling tool (9.33 and 9.46 per 10k words) and near zero after it for both, Fable taking about a week longer to reach zero; em-dashes and flattery openers vanish for both once the rules and hooks hold.

## Where the data cannot distinguish the models

The transcripts never run the two models on the same day except 11-06, and the Fable sessions of 09-20 to 09-23 (653 commits) have no transcript at all, so every transcript measure is a comparison of eras: rules, memory files, hooks, project maturity and Andy's own state all changed between them. Repository kind and model are entangled too: almost all hardware work is Fable before November and Opus 5.5 after it, and Opus 5 did almost none. The 7-day rework window is mostly unobserved for Opus 5.5. The judged samples are 45-120 per model and the correction counts are in single digits per type. Blinding removed names and trailers but not content: topic, date-bearing context and each model's prose style (Fable's declarative subjects) are visible, and every judge, like this author, is an Opus model judging Opus against Fable.

## A controlled head-to-head that would settle it

Give both models the same brief from the same commit, in separate git worktrees, with the same CLAUDE.md, memory, hooks and skills, in counterbalanced order, on 8-12 tasks drawn from the four kinds (a firmware library change with a harness, a KiCad edit with the kicad-text gates, a status or specification document, an NW-Sim part), each run twice per model. Measure: (1) test gates pass at the end (harness byte-identity, compile, `style_check.py`, kicad-cli ERC and net counts, nw-verify expected numbers) and the number of gate failures along the way; (2) commits, files per commit and a blinded ONE/MULTI rating; (3) defects found by a blinded reviewer (a different model family if possible, otherwise two Opus reviewers and agreement reported) given both diffs labeled A/B; (4) a scripted mid-task instruction (for example "end every report with the Summary form") and its compliance over the next N replies; (5) unverified numbers in the final report, checked against the session's tool outputs; (6) wall time, tokens and Andy's minutes spent. Score each task pairwise and report the per-task win count with its sign-test interval, which stays honest with a dozen tasks.
