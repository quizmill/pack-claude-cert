# Claude Cert Practice — quizmill learning pack

**Unofficial** practice question bank for the Claude Certified
Architect – Foundations (CCAR-F) exam — 310 scenario-based questions
across the five exam domains, single-answer and select-two, with
blueprint-weighted practice sessions, a full-length practice exam,
and a rationale for every option. Not affiliated with or endorsed by
Anthropic.

This is a learning pack for [quizmill](https://github.com/quizmill/quizmill),
the open-source practice-app engine: the pack is pure JSON, the engine
turns it into an installable, offline-first practice app with a
mistakes-review loop.

| Domain | Original | Purcell v2 | Total | Blueprint weight |
|---|---|---|---|---|
| Agentic Architecture & Orchestration | 68 | 16 | 84 | 27% |
| Tool Design & MCP Integration | 45 | 11 | 56 | 18% |
| Claude Code Configuration & Workflows | 50 | 12 | 62 | 20% |
| Prompt Engineering & Structured Output | 50 | 12 | 62 | 20% |
| Context Management & Reliability | 37 | 9 | 46 | 15% |
| **Total** | **250** | **60** | **310** | |

## Run it

```
git clone https://github.com/quizmill/quizmill
cd quizmill && npm install
npm run pack:use quizmill/pack-claude-cert
npm run dev
```

`npm run build` then produces a fully static app in `out/` — deploy it
to any static host and install it to your home screen (it works
offline).

## Sources & attribution

**Original bank (250).** Written for this pack against Anthropic's
public [*Claude Certified Architect – Foundations Exam Guide*](https://everpath-course-content.s3-accelerate.amazonaws.com/instructor%2F6nizmqk8tpzpfjvt6qmmav7rh%2Fpublic%2F1783542750%2FClaude+Certified+Architect+%E2%80%93+Foundations+Exam+Guide.pdf)
v1.0: its five domains at their blueprint weights, its task statements
and its six scenarios, with product facts checked against Anthropic's
public docs. About 180 questions are framed by the six scenarios and
the rest are standalone. Nothing is drawn from the live exam. Provenance is recorded in
[docs/provenance.md](docs/provenance.md).

**Matthew Purcell's paper (60).** The paper "CCAR-F practice exam v2" is
[Matthew Purcell's CCAR-F Practice Question Set v2](https://www.linkedin.com/posts/purcellmatthew_ccar-f-practice-exam-questions-v2-ugcPost-7491707994921938944-FhH5/),
credited in [NOTICE.md](NOTICE.md).

His questions are kept exactly as published. In the quizmill judge gate
(2026-10-31, `claude-opus-5-5`) the original bank passed with no fatal
or major findings; his 60 drew no fatal findings, 9 major and 30 minor.
One key, `cca-purcell-v2-2-3`,
relies on the skill field `allowed-tools` restricting Bash, while the
[Claude Code skills docs](https://code.claude.com/docs/en/skills) say it
pre-approves tools and does not restrict them. The details are in
[docs/provenance.md](docs/provenance.md).

The community-sourced bank this pack used to carry was retired with
bank v2; [NOTICE.md](NOTICE.md) records where it came from.

`python3 scripts/check-bank.py` checks the original bank for answer-key
tells (length, letter spread, absolute wording), blueprint balance and
stem overlap with retired material.

## Contributing

Corrections and new questions are welcome via PR. From a quizmill
checkout, validate your changes with:

```
npm run pack:validate /path/to/pack-claude-cert
```

Question ids are immutable once published (users' attempt history
points at them) — never renumber existing questions; add new ones.

## License

MIT — see [LICENSE](LICENSE). Upstream attribution in
[NOTICE.md](NOTICE.md).
