
Languages: [English](#llm-flow-dsl) | [中文](#中文简介) | [日本語](#日本語概要)
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
python -m llm_flow_dsl parse examples/support-triage.flow --pretty
python -m llm_flow_dsl run examples/support-triage.flow --input-json input.json --dry-run --pretty
```

Grammar reference: `docs/grammar-spec.md`

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- How to submit pull requests
- Code of Conduct

Early contributors will shape the DSL grammar and roadmap.

## License

llm-flow-dsl is released under the **MIT License**. See [LICENSE](LICENSE) for details.

This means you can:
- ✅ Use it freely in commercial projects
- ✅ Modify and distribute the code
- ✅ Use it without asking permission

With the condition that you:
- ⚠️ Include the original copyright notice

## Security

Found a security vulnerability? Please report it responsibly:
📧 See [SECURITY.md](SECURITY.md) for details.

## Support

- 📖 [Documentation](docs/)
- 🐛 [Report Issues](https://github.com/liliwen88/llm-flow-dsl/issues)
- 💬 [Discussions](https://github.com/liliwen88/llm-flow-dsl/discussions)

---

**Built with ❤️ by the llm-flow-dsl community**

## 中文简介

`llm-flow-dsl` 是一个面向生产环境的 **AI 规则引擎**。  
你可以用简洁、可读的 DSL，把 LLM 决策、业务约束、审批、重试和工具调用统一编排在同一条流程里。

核心目标：

- 让产品、运营也能读懂并参与规则设计
- 让工程团队可以版本化、测试化、可审计地发布 AI 流程
- 用确定性的业务规则约束模型输出，提升稳定性与可控性

一句话：

> 用业务级决策流程代码，交付可靠的 AI 功能。

## 日本語概要

`llm-flow-dsl` は、本番運用向けの **AI ルールエンジン** です。  
読みやすい小さな DSL で、LLM の判断、業務制約、承認、リトライ、ツール呼び出しを 1 つのフローとして記述できます。

主な狙い：

- プロダクト/オペレーション担当でもルールを理解・編集しやすい
- エンジニアがバージョン管理・テスト・監査可能な形で運用できる
- モデル出力だけに依存せず、決定論的な業務ルールで制御できる

一言で言うと：

> ビジネス品質の意思決定フローをコード化し、信頼できる AI 機能を提供する。
