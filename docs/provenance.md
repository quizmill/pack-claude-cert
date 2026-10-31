# Provenance audit

Every question in `questions.json` carries a `source` and a `sourceRef`.
This audit records where each part of the bank comes from and what it
permits.

## Current bank: bank v2 (from 2026-10-31)

| sourceRef | Questions | Licence | Status |
|---|---|---|---|
| Anthropic, *Claude Certified Architect – Foundations Exam Guide* v1.0, July 2026 (public PDF linked from the Anthropic Partner Academy certification page) | 245 (`ccar-f-*`) | The guide is the public reference for the exam. The questions are **original**: written against its task statements and its six scenarios, with new production situations, options and rationales. The guide's sample questions are not reproduced. Product behaviour (stop reasons, `tool_choice`, MCP scoping and errors, Claude Code memory, rules, skills and CLI flags, the Message Batches API) follows Anthropic's public docs. | Clear: original work, `source: original`. |
| Anthropic's public docs (platform.claude.com, code.claude.com) | 5 (`cca-q-*`) | Hand-written for this pack before bank v2 and kept, reworked to the v2 rules: new scenario ids, a rationale for every option, `sourceRef` reduced to the public doc page. | Clear: original work, `source: original`. |
| Matthew Purcell, *CCAR-F Practice Question Set v2* (LinkedIn) | 60 (`cca-purcell-v2-*`), paper `purcell-ccar-f-v2` | Used with the author's permission (#17). Not part of bank v2 and not changed by it. | Clear: credited in NOTICE.md. |

**Spec.** The guide fixes the shape: five domains weighted 27 / 18 / 20 /
20 / 15, six scenarios, four of which are dealt per sitting at about
fifteen questions each, single-answer and multiple-response items. The
original bank holds 68 / 45 / 50 / 50 / 37 questions per domain (250),
about 30 per scenario plus 70 standalone items for objectives the
scenarios do not reach, and 50 select-two items.

**No original practice paper.** A fixed 60-question paper drawn from the
bank (`ccar-f-practice-1`, scenarios 1, 2, 3 and 6 × 15) was built and
then dropped on 2026-10-31: its questions already appear in practice and
in the timed sitting, and Purcell's paper already gives learners a fixed
full-length sitting. The 60 questions stay in the bank.

**How it was written.** Each question was drafted against one task
statement, with the answer letter fixed in advance by a balanced plan so
that keys are spread across A–D and the ten select-two pairs. The
retired bank was never used as a template: authors worked from the guide
and the docs only, and a lint scored every draft stem against the retired
bank and Purcell's v2 stems so that a stem tracking either was rewritten
from a different angle.

## Retired bank (removed 2026-10-31)

| Source | Questions | Licence | Outcome |
|---|---|---|---|
| [Connectry-io/connectrylab-architect-cert-mcp](https://web.archive.org/web/20260321161626/https://github.com/Connectry-io/connectrylab-architect-cert-mcp/blob/master/LICENSE) (repository since deleted) | 390 | MIT (grant preserved by the Wayback Machine) | Retired. |
| [haytamAroui/Claude-Certified-Architect](https://github.com/haytamAroui/Claude-Certified-Architect) | 240 | MIT | Retired. |
| Hand-written here | 5 | this repo's | Kept, reworked (above). |

Purcell's v1 LinkedIn set (60 items) was removed earlier, in #14.

The MIT sources were licensed, so retiring them was a quality call, not
a legal one. A review on 2026-10-27 found answer keys that a test-wise
reader could spot from the options alone: the key was the longest option
in 82% and 95% of the two sources' items and sat on B in 47% and 82%;
there was not one select-two item; 56% of the bank was standalone rather
than scenario-framed; and the second source restated itself 66 times. A
judge model guessed the key from the options alone in 15 of 15 pilot
items. Fixing that in place was the same work as writing fresh.

The old questions had ids `cca-q-cn-*`, `cca-q-ha-*` and similar; the new
ones are `ccar-f-*`, so no attempt-history row can be mistaken for a
different question. XP, levels and stickers derive from attempts and
survive; the mistakes queue and readiness start again on the new ids.

## Checks

`scripts/check-bank.py` fails non-zero when the original bank breaks any
of:

- the key is the single longest option in more than 25% of single-answer
  items, or the single shortest in more than 30%; the mean key/distractor
  length ratio leaves 0.9–1.1
- the two select-two keys are the two longest options in more than 15% of
  select-two items (chance is 10%)
- key letters uneven across A–D; a select-two pair never used; select-two
  share outside 15–25%
- absolute wording only in distractors; "all/none of the above"
- a rationale that does not name the key and every distractor, or a
  distractor without its own explanation
- a domain more than one question from its blueprint share of 250; scenario
  counts more than three apart
- a stem with token Jaccard (lowercased words of four letters or more,
  markdown stripped) of 0.50 or more against any retired stem (read from
  git at `7ac5446`, never re-committed) or any of Purcell's v2 stems, or
  above 0.70 against another bank stem

**Result at 250 (2026-10-31).** Correct letters A 50 / B 50 / C 50 / D 50;
each of the ten select-two pairs five times. The key is the single
longest option in 17 of 200 single-answer items (8%) and the single
shortest in 44 (22%); mean key/distractor length ratio 1.01; select-two
keys are never the two longest. Domains 68 / 45 / 50 / 50 / 37; 30
questions per scenario plus 70 standalone. Every stem scores below 0.40
against the retired bank and below 0.50 against Purcell's v2 (one item
between 0.40 and 0.49); the closest two bank stems score 0.35. Each
question links one of 29 concept cards (one per task statement; 2.2
and 5.3, both about error reporting, share one).

After the judge pass below: the key is the single longest in 20 of 200
(10%), single shortest in 45 (22%); every other figure is unchanged.

**Judge gate (2026-10-31).** The quizmill/admin `evals` gate ran over all
310 questions with `claude-opus-5-5` (the gate's own model was not
available on the account that night) and the thresholds of `gate.json`:
every question, all three passes (solve, choices-only, review), 930
verdicts.

| | first run, 310 | after rework, 310 | after rework, original 250 |
| --- | --: | --: | --: |
| fatal | 0 | 0 | 0 |
| major | 14 (5 original, 9 Purcell) | 9 (Purcell) | 0 |
| key not confirmed | 1 (Purcell) | 3 (2 original, 1 Purcell) | 2 |
| solve disagrees with key | 0 | 1 (original) | 1 |
| minor | 24% (43 original, 30 Purcell) | 13% (9 original, 30 Purcell) | 4% |

All 48 flagged original items were reworked against the judge's flaw. Five
items (and the commands-and-skills card) described the skill frontmatter
field `allowed-tools` as a restriction; the Claude Code skills reference
says it pre-approves tools and "does not restrict which tools are
available", and `disallowed-tools` removes tools while a skill is active.
Those items now say so and cite the reference. The three original items
still flagged (`ccar-f-s2-12`, `ccar-f-s4-02`, `ccar-f-s5-10`) carry no
flaw: the judge cannot confirm `disallowed-tools` from its own knowledge
and, on `ccar-f-s4-02`, picks `allowed-tools` as the restriction. The
current docs settle both in the bank's favour. Purcell's items are left
as published.

**Gate decision (2026-10-31).** The pack ships with the judge gate read on
the original 250. Purcell's 60 are not changed: their findings (9 major,
30 minor, 1 key not confirmed; among them `cca-purcell-v2-2-3`, whose key
relies on `allowed-tools` restricting Bash) are noted in `README.md`.

Choices-only: the judge picks the key from the options alone in 100% of
items (the Professional bank: 99%). An expert reader can tell good
practice from bad practice without the stem, so this figure says little
about cueing in this domain; the length and letter gates above are the
cueing checks.

**Not yet done.** A human read of the bank with `/review`.

## Reproduce

```
npx quizmill validate .
python3 scripts/check-bank.py
```
