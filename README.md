# Claude Cert Practice — quizmill learning pack

**Unofficial** practice question bank for the Claude Certified
Architect (Foundations) exam — 635 multiple-choice questions across the
five exam domains, with blueprint-weighted practice sessions, scenario
case studies, and per-question explanations. Not affiliated with or
endorsed by Anthropic.

This is a learning pack for [quizmill](https://github.com/quizmill/quizmill),
the open-source practice-app engine: the pack is pure JSON, the engine
turns it into an installable, offline-first practice app with a
mistakes-review loop.

| Domain | Questions | Blueprint weight |
|---|---|---|
| Agentic Architecture & Orchestration | 143 | 27% |
| Prompt Engineering & Structured Output | 139 | 20% |
| Context Management & Reliability | 131 | 15% |
| Claude Code Configuration & Workflows | 115 | 20% |
| Tool Design & MCP Integration | 107 | 18% |

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

The bank is curated from MIT-licensed community question sets, plus a
small number of hand-written questions grounded in Anthropic's public
documentation:

| Source | Questions | License |
|---|---|---|
| [haytamAroui/Claude-Certified-Architect](https://github.com/haytamAroui/Claude-Certified-Architect) | 240 | MIT |
| [Connectry-io/connectrylab-architect-cert-mcp](https://github.com/Connectry-io/connectrylab-architect-cert-mcp) | 390 | MIT |
| Hand-authored from the [Anthropic docs](https://docs.anthropic.com/) and exam guide | 5 | this repo's |

Every question carries a `sourceRef` URL pointing at its upstream
origin, and the app links to it in the answer panel. Upstream license
texts are preserved in [NOTICE.md](NOTICE.md).

Questions sourced from repos without an open-source license were
excluded from this pack.

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
