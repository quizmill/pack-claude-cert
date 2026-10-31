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

**Practice paper.** `ccar-f-practice-1` ("CCAR-F practice exam 1") is 60
of the scenario questions: scenarios 1, 2, 3 and 6 × 15, weighted
16 / 11 / 12 / 12 / 9 across the domains, 12 of them select-two. Its
questions sit together at the start of `questions.json` and carry
`level: exam` like every scenario question.

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
- key letters uneven across A–D; a select-two pair never used; select-two
  share outside 15–25%
- absolute wording only in distractors; "all/none of the above"
- a rationale that does not name the key and every distractor, or a
  distractor without its own explanation
- a domain more than one question from its blueprint share of 250; scenario
  counts more than three apart
- the practice paper not four scenarios × 15, not contiguous or not all at
  level `exam`
- a stem with token Jaccard (lowercased words of four letters or more,
  markdown stripped) of 0.50 or more against any retired stem (read from
  git at `7ac5446`, never re-committed) or any of Purcell's v2 stems, or
  above 0.70 against another bank stem

## Reproduce

```
npx quizmill validate .
python3 scripts/check-bank.py
```
