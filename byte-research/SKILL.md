---
name: byte-research
description: Research competitors, alternatives, pricing, market trends, user complaints, and product opportunities for Your ByteDance / Byte OS. Use when the user asks for competitor benchmarking, market intelligence, online research, product iteration based on external signals, or refreshed research for an existing `.byte-os/` project.
---

# Byte Research

Research supplies the external world signal for Your ByteDance. It must use current sources for market, competitor, pricing, and trend claims.

## Required Behavior

Browse the web when researching modern products, competitors, pricing, market trends, app reviews, changelogs, or "latest" activity. Cite sources with links in the output artifacts.

Prefer:

- Official product pages
- Docs and changelogs
- Pricing pages
- App store listings and reviews
- Public roadmaps
- Credible industry articles
- GitHub repositories for developer tools

Avoid unsupported claims, stale assumptions, and invented user feedback.

## Workflow

1. Read current context:

```text
.byte-os/BYTE.md
.byte-os/STATUS.md
.byte-os/PRODUCT_SPEC.md
.byte-os/ROADMAP.md
```

2. Identify research questions:

- What products solve the same problem?
- What adjacent tools are substitutes?
- How do competitors price and package value?
- What are users praising or complaining about?
- What features are becoming table stakes?
- Where is there room for differentiation?
- Which assumptions in `OKRS.md` need evidence?

3. Search and compare:

- Direct competitors
- Indirect substitutes
- Adjacent workflow tools
- Open-source or low-cost alternatives
- Pricing and packaging
- Onboarding and activation patterns
- Recent product updates

4. Synthesize:

- Keep facts separate from inference.
- Convert findings into product implications.
- Mark "copy", "adapt", "avoid", and "differentiate" opportunities.
- Record confidence level and evidence quality.
- Prefer direct product evidence over commentary when available.

## Artifacts

Write or update:

```text
.byte-os/RESEARCH.md
.byte-os/COMPETITORS.md
.byte-os/DECISIONS.md
.byte-os/STATUS.md
```

`COMPETITORS.md` should include:

```text
| Product | Positioning | Key features | Pricing | Strength | Weakness | Source |
```

`RESEARCH.md` should include:

- Research date
- Search scope
- Key findings
- User complaint patterns
- Product opportunities
- Risks and caveats
- Recommended impact on roadmap

Update `STATUS.md` using the shared Byte OS state contract with
`stage: researched`, `current_workflow: byte-research`, and the next safe
workflow derived from the shared state resolver.

## Completion Criteria

Research is complete when the next product decision can name what the market already does, what users seem to value, and where this product should be different.
