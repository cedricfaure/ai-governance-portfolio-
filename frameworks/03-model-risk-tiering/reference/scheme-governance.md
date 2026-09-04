> Component of the [Model Risk Tiering Scheme](../README.md) framework.

# Re-tiering triggers and governance of the scheme itself

## Re-tiering triggers

Tiering is not an annual exercise. It is event-driven, with a periodic backstop.

**Mandatory immediate re-tier:**

- Change in the decision or action the system influences
- Expansion of scope: new population, new jurisdiction, new use
- Change in autonomy or action scope
- Material change in volume, exposure or materiality
- Change to the underlying model, including a supplier-side update
- Change in data sources, categories or lawful basis
- A new or amended regulatory obligation brought into scope
- Any incident, near-miss, or upheld challenge to an outcome
- Failure of a control on which mitigation credit was granted
- Change in a dependency's tier
- Loss of the named owner

**Periodic backstop:** at each tier's revalidation cadence, regardless of whether a trigger fired.

The supplier-update trigger deserves emphasis. Where a system depends on a third-party model, the supplier's release schedule is now part of your change-control surface. If the contract does not provide change notification, D10 scores 4 or 5 and the framework will tier accordingly — which is the correct commercial signal to send.

## Governance of the scheme itself

Assessment is performed by the process owner and reviewed by a second party. Self-assessment without review reliably produces low tiers.

Dimension anchors are frozen between calibration cycles. Amending an anchor after seeing where a system lands is the corruption this scheme is most exposed to.

The rule set is versioned. Every assessment records the rule-set version that produced it. Changing the rules does not silently re-tier the estate; it produces a controlled re-run with a diff.

Appeals are permitted and logged. A sponsor may challenge a tier. The challenge, its resolution and its reasoning are recorded. Appeals are a data source for calibration, not a nuisance.

Overrides are permitted only upward without limit, and downward never. A reviewer may raise a tier on judgement. Lowering below what the rules produce requires the T4 approval authority and a minuted rationale, and is reported.

Annual calibration. Compare the tier distribution against incidents and near-misses. If incidents concentrate in T2, the anchors are miscalibrated — fix the anchors, not the incident record.
