# llm-flow-dsl

AI + Business DSL as an AI rules engine.

AI + Business DSL for production workflows.

`llm-flow-dsl` is an **AI rules engine**: use a small, readable DSL to orchestrate LLM decisions, business constraints, approvals, retries, and tool calls in one place.

## Why this can win

Most AI demos fail in production because teams cannot express policy, risk control, and business logic around LLM calls.

`llm-flow-dsl` focuses on the missing layer:

- Product teams can read and edit flow rules.
- Engineering teams can version, test, and release safely.
- AI behavior is governed by deterministic business rules.

## Positioning

- Not "just another prompt framework".
- Not "just workflow automation".
- It is a **domain language for AI decisions under business constraints**.

One-line pitch:

> Ship reliable AI features by writing business-grade decision flows as code.

## Core design principles

- **Readable first**: PM/ops can understand every rule.
- **Deterministic guardrails**: model output is never the only source of truth.
- **Production-native**: retries, fallback models, approvals, audit log.
- **Testable**: every flow can run in CI with fixtures.

## MVP scope (v0.1)

- DSL parser for flow blocks:
  - `input`
  - `route`
  - `llm`
  - `if/else`
  - `tool`
  - `approval`
  - `output`
- Local runner:
  - execute flow end-to-end
  - structured logs per step
  - dry-run mode
- Validation:
  - schema checks
  - unknown symbol checks
  - unsafe config checks
- Tests:
  - golden tests for flow outputs
  - deterministic fixtures for model/tool stubs

## Killer first use-cases

- AI customer support triage with escalation policy
- AI sales lead qualification with compliance gates
- AI content moderation with region-specific rules
- AI internal copilot actions requiring approval workflow

## Growth playbook (how to make it "hot")

1. Build one flagship demo that solves a painful business problem.
2. Open-source 10 practical flow templates by industry.
3. Publish "before/after" reliability metrics (not just flashy demos).
4. Launch a no-code visualizer for DSL execution traces.
5. Push weekly content: failure cases, guardrail patterns, production lessons.

## 30-day launch plan

1. Week 1: parser + runner + one real template.
2. Week 2: test harness + trace viewer CLI output.
3. Week 3: docs site + 3 industry examples.
4. Week 4: public launch + live teardown of real user flow.

## Project structure (initial)

```text
llm-flow-dsl/
  README.md
  docs/
    product-strategy.md
    roadmap.md
  examples/
    support-triage.flow
```

## Quick start (placeholder)

```bash
# coming soon
```

## Contributing

PRs and design feedback are welcome. Early contributors will shape the DSL grammar.
