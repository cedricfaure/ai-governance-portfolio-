> Component of the [AI Use Case Business Card](../README.md) framework.

# KPI library and non-financial value

## The KPI ladder

Five layers. Every use case declares at least one KPI per layer, each with an owner, a baseline, a target, a threshold and a measurement method. A use case with no Layer 3 KPI is a tool deployment, not a business case.

| Layer | Question it answers | Owner | Example KPIs |
|---|---|---|---|
| **L5 Technical** | Is the system reliable, safe and affordable? | Data science / engineering | Output quality score, hallucination / error rate, p95 latency, cost per interaction, drift indicator |
| **L4 Adoption** | Are people using and trusting it? | Product / frontline ops | Workflow penetration, weekly active eligible users, acceptance rate, override rate |
| **L3 Operational** | Is the work actually getting better? | Named process owner | Cycle time, cost per case, first-contact resolution, rework rate, throughput per FTE |
| **L2 Strategic** | Is business performance shifting? | BU lead / strategy | Customer satisfaction, on-time delivery, retention, compliance performance, service coverage |
| **L1 Financial** | Is enterprise value being created? | Finance / FP&A | Net benefit vs TCO, cost-to-serve, incremental revenue, payback period, risk-adjusted NPV |

**Rule:** L1 and L2 do not move first. Expecting financial signal at pilot stage causes premature termination of good use cases and premature scaling of bad ones. Gate on the layer appropriate to the phase.

## KPI computation methods

Definitions must be fixed **before** the pilot. Redefining a KPI mid-flight destroys the comparison and is the most frequent cause of a business case that cannot be audited.

**Workflow penetration (L4)**

`= eligible tasks completed with AI support ÷ total eligible tasks, in period`

Define "eligible" explicitly and freeze it. Growing the eligible denominator mid-programme is a common way to make adoption look worse than it is; shrinking it is a common way to flatter it.

**Acceptance rate (L4)**

`= outputs accepted with no or trivial edit ÷ total outputs generated`

Define "trivial" with an edit-distance threshold or a rubric. Track override rate separately — a high override rate with good outcomes may indicate healthy human oversight rather than a failing model.

**Cycle time (L3)**

`= median (not mean) end-to-end elapsed time per case`

Use median plus p90. Means hide the tail, and the tail is where AI failure modes concentrate. Measure **end-to-end**, including any new verification steps — measuring only the accelerated sub-step is how the verification tax gets hidden.

**Cost per case (L3)**

`= (labour cost + system cost + rework cost) ÷ cases completed`

Rework cost is mandatory. A system that produces faster wrong answers reduces cost per case on a naive calculation.

**Throughput per FTE (L3)**

`= completed units ÷ FTE-hours worked`

Report **by experience cohort**, minimum: least-experienced tertile, middle, most-experienced tertile. The evidence base shows benefit concentrating in lower-experience cohorts and occasionally reversing in the most experienced. A single blended figure conceals both the largest gain and the largest risk.

**Net benefit and risk-adjusted ROI (L1)**

```
Gross Benefit        = Σ (B1..B4, B6) realised in period
Risk Delta           = Σ (ALE_before − ALE_after) across all identified scenarios
                       positive = net risk reduction (a benefit)
                       negative = net risk increase (a cost)
TCO                  = Build + Run + Governance + Reserve  (see Block 7)
Risk-Adjusted Net Benefit = Gross Benefit + Risk Delta − TCO
Risk-Adjusted ROI (%)     = Risk-Adjusted Net Benefit ÷ TCO × 100
Payback period            = first period in which cumulative Risk-Adjusted
                            Net Benefit ≥ 0
```

Where `ALE = Single Loss Expectancy × Annualised Rate of Occurrence`, estimated per scenario. Risk-increase scenarios must include, at minimum: model drift, erroneous output reaching a customer or citizen, bias or discriminatory outcome, data leakage, and regulatory non-compliance where the system falls in scope of an applicable regime.

**Presentation rule:** report **P10 / P50 / P90**, never a single figure. A point estimate is a claim of precision the underlying data does not support. The P10 case is what the sponsor should be willing to be held to.

## Non-financial and public value

Three tiers, following established public-sector appraisal practice. All three are recorded; only Tier 1 enters the financial model.

| Tier | Definition | Treatment |
|---|---|---|
| **1 — Monetisable** | Can be credibly expressed in currency | Enters the financial case |
| **2 — Quantifiable, not monetised** | Measurable in natural units, no defensible price | Stated with baseline, target and unit; presented alongside the financial case, never inside it |
| **3 — Qualitative** | Real but not measurable | Described in one sentence with the reason it resists quantification |

**Tier 2 natural units — worked examples of acceptable formulations:**

- Waiting time: median days from referral to appointment — baseline 34, target 21
- Access equity: share of applications completed without assisted support, by segment
- Service coverage: proportion of eligible population reached
- Safety: number of near-miss events detected before escalation
- Resilience: mean time to detect and mean time to recover
- Workforce: proportion of staff hours on statutorily required vs discretionary activity
- Sustainability: energy or emissions per unit of service delivered
- Trust: appeal or complaint rate against automated decisions

**Rules:**

1. Tier 3 alone never justifies funding.
2. A Tier 2 benefit must have a baseline. "Improved citizen experience" without a measure is Tier 3, however it is phrased.
3. Where a public body's mandate makes a Tier 2 outcome the primary objective, say so explicitly and present the financial case as a **constraint** (affordability) rather than the **objective** (value for money). Do not disguise a mission case as a savings case — it fails at the first audit.
4. Never convert a Tier 2 benefit to currency using an invented shadow price. If a published, citable valuation exists in the relevant jurisdiction, use it and cite it. Otherwise it stays Tier 2.
