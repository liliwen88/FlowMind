# Product Strategy

## North Star

Become the default way teams encode AI behavior with business constraints.

## Target users

- AI engineers shipping LLM-backed features
- Platform/backend teams responsible for reliability
- Product/ops teams defining business policy

## Main problem

Teams can build prompts fast, but cannot safely scale AI decisions because:

- rules are spread across prompts, code, and dashboards
- changes are hard to review
- failures are difficult to audit

## Wedge strategy

Start with one narrow but high-value workflow:

- inbound support ticket triage
- strict escalation rules
- measurable ROI (faster response + lower wrong-routing rate)

## Differentiation

- Business-readable DSL
- Built-in control primitives (`approval`, `fallback`, `policy`)
- Test and replay support for incident response

## Distribution

- Open-source core DSL + runner
- “Template library” as growth engine
- Integration guides for common stacks

## Monetization options (later)

- Hosted control plane (execution trace UI, policy governance)
- Enterprise policy packs
- Team collaboration and approval workflows

