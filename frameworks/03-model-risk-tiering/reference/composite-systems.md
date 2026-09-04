> Component of the [Model Risk Tiering Scheme](../README.md) framework.

# Composite systems and aggregate risk

The revised MRM guidance identifies aggregate model risk arising from dependencies across models — shared data, shared assumptions, shared methodologies. Agentic architectures make this sharply worse: systems now invoke systems, at machine speed, without a human between them.

## Inheritance rules

1. **Downstream inheritance.** A system consuming another's output inherits the maximum of its own and the upstream system's scores on D7 (opacity), D9 (volatility) and D10 (third-party dependency). You cannot be more certain than your inputs.
2. **Consequence flows down, not up.** A benign upstream component feeding a consequential downstream decision does not raise the upstream tier on Family A. But it must be recorded as a dependency of a higher-tier system and inherits that system's change-control and notification obligations — because changing it changes the consequential system.
3. **Orchestrator rule.** A system that invokes others is tiered on the union of all actions reachable through it, including transitively. An orchestrator with access to one T4-capable action is T4. Composition does not dilute; it accumulates.
4. **Chain length.** Chains of three or more autonomous invocations without an intervening human checkpoint add +1 to D4, capped at 5.
5. **Common-mode dependency.** Where three or more T3+ systems share a component — the same foundation model, the same feature pipeline, the same reference dataset — that component is registered as a critical dependency and tiered at the maximum of its dependants, irrespective of its own standalone score.

Rule 5 is the one organisations discover late. A shared embedding pipeline scoring T1 on its own merits, on which six T3 systems depend, is a single point of failure with T3 consequence. Standalone tiering will never surface it. The dependency graph must be maintained, and it must be queried.
