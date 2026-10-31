#!/usr/bin/env python3
"""Curation checks for questions.json that the engine validator does not do.

The engine's `quizmill validate` checks the schema and cross-references.
This script checks the original bank (`source: original`) for the things a
test-wise candidate exploits, and for drift back towards retired material:

  * the correct option must not be systematically the longest one, nor
    systematically the shortest; mean length ratio key/distractors 0.9–1.1
  * correct letters spread across A–D, every select-two pair used
  * absolute wording ("always", "only", ...) not only in distractors; no
    "all/none of the above"
  * every question has an explanation that names the key and every
    distractor, and a per-option explanation on each distractor
  * the domain split is within one question of the manifest weights, and
    the six scenarios hold counts within three of each other
  * the practice paper is 60 questions, four scenarios × 15, together in
    bank order and all at level `exam`
  * no stem tracks the retired bank or Matthew Purcell's v2 paper (token
    Jaccard < 0.50 against every stem), and no two stems are near-copies
    (Jaccard <= 0.70); the retired bank is read from git history so it is
    never committed again

Run from the pack root:  python3 scripts/check-bank.py
Exit code is non-zero when a check fails.
"""
import collections
import itertools
import json
import re
import statistics
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
bank = json.loads((ROOT / "questions.json").read_text())
manifest = json.loads((ROOT / "pack.json").read_text())
weights = {c["key"]: c["weight"] for c in manifest["categories"]}

# The last commit before bank v2: its questions.json is the retired bank.
RETIRED_AT = "7ac5446"
RETIRED_LIMIT = 0.50
SIBLING_LIMIT = 0.70
PURCELL_PREFIX = "cca-purcell-"
# Doc-grounded originals written for the retired bank and kept in v2 under
# their old ids; each is exempt from overlap with its own earlier version.
KEPT = {
    "cca-q-tool-desc-routing",
    "cca-q-escalation-triggers",
    "cca-q-strict-tool-use",
    "cca-q-subagent-summary-shape",
    "cca-q-subagent-tool-restriction",
}
PAPER = "ccar-f-practice-1"
BANK_SIZE = 250

failures: list[str] = []
warnings: list[str] = []
qs = [q for q in bank if q["source"] == "original"]
n = len(qs)

# --- answer-position balance ------------------------------------------------
single = [q for q in qs if "correctKey" in q]
multi = [q for q in qs if "correctKeys" in q]
letters = collections.Counter(q["correctKey"] for q in single)
print(f"original questions: {n}  single-answer: {len(single)}  select-two: {len(multi)}")
print("correct letter (single-answer):", dict(sorted(letters.items())))
if single:
    expected = len(single) / 4
    for k in "ABCD":
        if abs(letters.get(k, 0) - expected) > max(3, 0.1 * expected):
            failures.append(f"letter {k} is correct {letters.get(k, 0)} times (expected about {expected:.0f})")
pairs = collections.Counter("+".join(sorted(q["correctKeys"])) for q in multi)
print("correct pair (select-two):", dict(sorted(pairs.items())))
if multi:
    unused = ["+".join(p) for p in itertools.combinations("ABCDE", 2) if "+".join(p) not in pairs]
    if unused:
        failures.append(f"select-two pairs never used: {', '.join(unused)}")
    share_two = len(multi) / n
    if not 0.15 <= share_two <= 0.25:
        failures.append(f"select-two is {share_two:.0%} of the bank (want about a fifth)")
for q in multi:
    if len(q["correctKeys"]) != 2 or len(q["options"]) != 5:
        failures.append(f"{q['id']}: select-two needs 2 keys and 5 options")
    if "Select TWO" not in q["prompt"]:
        failures.append(f"{q['id']}: select-two prompt does not say (Select TWO.)")
for q in single:
    if len(q["options"]) != 4:
        failures.append(f"{q['id']}: single-answer question with {len(q['options'])} options")

# --- length tell -------------------------------------------------------------
longest = shortest = 0
ratios = []
for q in single:
    lengths = {o["key"]: len(o["text"]) for o in q["options"]}
    ck = q["correctKey"]
    ordered = sorted(lengths.values(), reverse=True)
    if lengths[ck] == ordered[0] and ordered[0] > ordered[1]:
        longest += 1
    if lengths[ck] == ordered[-1] and ordered[-1] < ordered[-2]:
        shortest += 1
    others = [v for k, v in lengths.items() if k != ck]
    ratios.append(lengths[ck] / statistics.mean(others))
for q in multi:
    lengths = {o["key"]: len(o["text"]) for o in q["options"]}
    correct = [lengths[k] for k in q["correctKeys"]]
    wrong = [v for k, v in lengths.items() if k not in q["correctKeys"]]
    ratios.append(statistics.mean(correct) / statistics.mean(wrong))
    if min(correct) > max(wrong):
        warnings.append(f"{q['id']}: every correct option is longer than every distractor")
if single:
    share = longest / len(single)
    short_share = shortest / len(single)
    mean_ratio = statistics.mean(ratios)
    print(f"key is the single longest: {longest}/{len(single)} ({share:.0%}); "
          f"single shortest: {shortest} ({short_share:.0%}); mean length ratio key/others: {mean_ratio:.2f}")
    if share > 0.25:
        failures.append(f"key is the longest option in {share:.0%} of single-answer questions (limit 25%)")
    if short_share > 0.30:
        failures.append(f"key is the shortest option in {short_share:.0%} of single-answer questions (limit 30%)")
    if not 0.9 <= mean_ratio <= 1.1:
        failures.append(f"keys average {mean_ratio:.2f}x the length of distractors (want 0.90–1.10)")

# --- wording tells -----------------------------------------------------------
ABSOLUTE = re.compile(r"\b(always|never|all|none|every|only|guarantee[sd]?)\b", re.I)
abs_in_correct = abs_in_wrong = 0
for q in qs:
    keys = {q["correctKey"]} if "correctKey" in q else set(q["correctKeys"])
    for o in q["options"]:
        if ABSOLUTE.search(o["text"]):
            if o["key"] in keys:
                abs_in_correct += 1
            else:
                abs_in_wrong += 1
        if re.search(r"all of the above|none of the above", o["text"], re.I):
            failures.append(f"{q['id']}: 'all/none of the above' option")
print(f"absolute words — in keys: {abs_in_correct}, in distractors: {abs_in_wrong}")
if abs_in_wrong and not abs_in_correct:
    failures.append("absolute wording appears only in distractors — a test-wise tell")

# --- per-question hygiene ----------------------------------------------------
for q in qs:
    keys = [q["correctKey"]] if "correctKey" in q else q["correctKeys"]
    exp = q["explanation"]
    for o in q["options"]:
        if not re.search(rf"\b{o['key']}\b", exp):
            what = "the key" if o["key"] in keys else "distractor"
            failures.append(f"{q['id']}: explanation does not name {what} {o['key']}")
        if o["key"] not in keys and not o.get("explanation"):
            failures.append(f"{q['id']}: distractor {o['key']} has no per-option explanation")
    if not q.get("tags"):
        failures.append(f"{q['id']}: no tags")
    texts = [o["text"].strip().lower() for o in q["options"]]
    if len(set(texts)) != len(texts):
        failures.append(f"{q['id']}: duplicate option text")
    if q.get("scenarioId") and q.get("level") != "exam":
        failures.append(f"{q['id']}: scenario-framed question is not at level exam")
    if not q.get("scenarioId") and q.get("level"):
        failures.append(f"{q['id']}: standalone question carries a level")

# --- distribution ------------------------------------------------------------
by_cat = collections.Counter(q["categoryKey"] for q in qs)
print(f"domain split vs blueprint (at {BANK_SIZE}):")
for key, w in weights.items():
    target = w * BANK_SIZE
    have = by_cat.get(key, 0)
    flag = "" if abs(have - target) <= 1 else "  <-- more than one question off"
    print(f"  {key:24s} {have:4d}  target {target:5.1f}{flag}")
    if abs(have - target) > 1:
        failures.append(f"{key}: {have} questions, blueprint wants {target:.1f} (±1)")
if n != BANK_SIZE:
    failures.append(f"bank holds {n} original questions, want {BANK_SIZE}")
by_scen = collections.Counter(q["scenarioId"] for q in qs if q.get("scenarioId"))
print("per scenario:", dict(sorted(by_scen.items())), " standalone:", n - sum(by_scen.values()))
if len(by_scen) != 6:
    failures.append(f"{len(by_scen)} scenarios used, want 6")
elif max(by_scen.values()) - min(by_scen.values()) > 3:
    failures.append("per-scenario counts differ by more than three")

# --- practice paper ----------------------------------------------------------
positions = [i for i, q in enumerate(bank) if q.get("paperId") == PAPER]
paper = [bank[i] for i in positions]
paper_scen = collections.Counter(q.get("scenarioId") for q in paper)
print(f"paper {PAPER}: {len(paper)} questions;", dict(sorted(paper_scen.items())),
      f"select-two {sum('correctKeys' in q for q in paper)};",
      dict(sorted(collections.Counter(q["categoryKey"] for q in paper).items())))
if len(paper) != 60 or len(paper_scen) != 4 or set(paper_scen.values()) != {15}:
    failures.append(f"paper {PAPER} must be four scenarios × 15 questions")
if positions and positions[-1] - positions[0] + 1 != len(positions):
    failures.append(f"paper {PAPER} questions are not together in bank order")
if any(q.get("level") != "exam" for q in paper):
    failures.append(f"paper {PAPER} has questions outside level exam")
if paper:
    for key, w in weights.items():
        have = sum(q["categoryKey"] == key for q in paper)
        if abs(have - w * 60) > 1.5:
            failures.append(f"paper {PAPER}: {key} has {have}, blueprint wants {w * 60:.1f}")

# --- stem overlap ------------------------------------------------------------
def tokens(text: str) -> set[str]:
    text = re.sub(r"[`*_#>\[\]()]", " ", text)
    return set(re.findall(r"[a-z]{4,}", text.lower()))


def jaccard(a: set[str], b: set[str]) -> float:
    return len(a & b) / len(a | b) if a | b else 0.0


try:
    old_bank = json.loads(subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{RETIRED_AT}:questions.json"],
        check=True, capture_output=True, text=True).stdout)
except (subprocess.CalledProcessError, FileNotFoundError):
    old_bank = None
    failures.append(f"cannot read the retired bank from git ({RETIRED_AT}:questions.json); "
                    "run from a full clone")
stems = {q["id"]: tokens(q["prompt"]) for q in qs}
purcell = {q["id"]: tokens(q["prompt"]) for q in bank if q["id"].startswith(PURCELL_PREFIX)}


def gate(label: str, others: dict[str, set[str]]) -> None:
    bands = collections.Counter()
    for qid, t in stems.items():
        cands = [(oid, jaccard(t, ot)) for oid, ot in others.items() if oid != qid]
        best_id, best = max(cands, key=lambda p: p[1])
        bands["0.50+" if best >= 0.50 else "0.40-0.49" if best >= 0.40 else "<0.40"] += 1
        if best >= RETIRED_LIMIT:
            failures.append(f"{qid}: stem overlap {best:.2f} with {label} {best_id} (limit <{RETIRED_LIMIT:.2f})")
    print(f"stem overlap vs {label} ({len(others)} items):",
          {k: bands[k] for k in ("0.50+", "0.40-0.49", "<0.40")})


if old_bank is not None:
    retired = {q["id"]: tokens(q["prompt"]) for q in old_bank if not q["id"].startswith(PURCELL_PREFIX)}
    gate("retired", retired)
if purcell:
    gate("Purcell v2", purcell)
ids = sorted(stems)
top_pair = (0.0, "", "")
for i, a in enumerate(ids):
    for b in ids[i + 1:]:
        s = jaccard(stems[a], stems[b])
        top_pair = max(top_pair, (s, a, b))
        if s > SIBLING_LIMIT:
            failures.append(f"{a} / {b}: stem overlap {s:.2f} (limit {SIBLING_LIMIT:.2f})")
print(f"highest stem overlap between bank items: {top_pair[0]:.2f} ({top_pair[1]} / {top_pair[2]})")

print("difficulty:", dict(sorted(collections.Counter(q["difficulty"] for q in qs).items())))
print("reviewStatus:", dict(collections.Counter(q["reviewStatus"] for q in qs)))
print("source (whole pack):", dict(collections.Counter(q["source"] for q in bank)))

for w in warnings:
    print("warning:", w)
for f in failures:
    print("FAIL:", f)
print("OK" if not failures else f"{len(failures)} failure(s)")
sys.exit(1 if failures else 0)
