> Component of the [AI Use Case Business Card](../README.md) framework.

# Baselining — the core discipline

Most AI business cases fail here, and it is the single field that most distinguishes a credible card from a plausible one. The card therefore carries an explicit **Baseline Confidence Grade**, and that grade **caps how much projected benefit may be entered into the financial plan.**

## Baseline Confidence Grades

| Grade | Method | Description | Benefit booking cap |
|---|---|---|---|
| **A** | System-derived historical data | ≥12 months of transaction-level data from the operational system, covering the exact metric | **100% of P50** |
| **B** | Process mining | Event-log-derived process performance, ≥3 months, covering ≥80% of case volume | **85% of P50** |
| **C** | Time-motion study | Structured observation, 2–4 weeks, statistically sampled across roles, shifts and case types | **70% of P50** |
| **D** | Structured expert elicitation | Three-point (optimistic / likely / pessimistic) estimates from ≥5 independent practitioners, aggregated, with dispersion reported | **50% of P50** |
| **E** | External benchmark only | Industry figures, vendor claims or published studies, with no internal measurement | **0% — indicative only** |

**The booking cap is the mechanism.** It converts baseline quality from an abstract virtue into a number the sponsor cares about, which is what makes teams actually go and measure. It also means a Grade E use case can still be *approved* — but only for a baselining sprint, never for a build.

## The hard rule

**No use case passes the Build gate at Grade E.** If the baseline does not exist, the first funded activity is establishing it.

## When no baseline exists — the mitigation ladder

Work down this list. Stop at the first feasible option.

1. **Reconstruct from adjacent systems.** Ticketing, workflow, ERP, HRIS, case management and telephony systems frequently hold the answer even when nobody has ever reported it. Timestamps are a baseline. This is underused and should always be checked first.
2. **Run a two-to-four week time-motion study before build.** Cheap, fast, and moves the case from Grade D/E to Grade C — often the single highest-return two weeks in the whole programme.
3. **Instrument first, build second.** Where the process is digital but unmeasured, deploy measurement into the current workflow and run it for one full cycle before any AI is introduced. This creates a clean pre-period.
4. **Use a hold-out cohort.** Where a pre-period is impossible, preserve a randomly assigned control group at deployment. This substitutes a concurrent comparison for a historical one and is methodologically stronger than a pre/post baseline.
5. **Use staggered rollout.** Where a permanent hold-out is unacceptable, sequence deployment across teams, sites or regions and compare early against not-yet-deployed groups. Every unit eventually receives the system, so this is usually the most politically acceptable rigorous design.
6. **Structured expert elicitation, honestly labelled.** Three-point estimates from at least five independent practitioners, aggregated, with the spread reported. Grade D. Adequate to justify a pilot; never adequate to justify a scaling decision.
7. **External benchmark with a mandatory haircut.** Grade E. Apply the optimism-bias adjustment in full (below), mark the benefit as indicative, and attach a baselining sprint as the first deliverable.

## Attribution design

Baseline answers "compared to what?". Attribution answers "how do we know it was us?". State one of the following on the card:

| Design | Strength | When to use |
|---|---|---|
| Randomised control | Strongest | Feasible where users or cases can be randomly assigned |
| Staggered rollout (difference-in-differences) | Strong | Multi-site or multi-team deployment |
| Hold-out cohort | Strong | Where a permanent control group is acceptable |
| Synthetic control | Moderate | Where a comparable untreated unit can be constructed |
| Pre/post with exogenous controls | Weak | Only where the above are genuinely impossible — state why |
| Pre/post, uncontrolled | Not acceptable for scaling decisions | Pilot learning only |

**Prohibited as a primary KPI:** self-reported time savings, self-reported productivity, and user satisfaction surveys used as a proxy for productivity. The evidence is unambiguous that perceived and actual productivity can diverge sharply and in the wrong direction. These may be collected as supporting signal; they may not carry the case.

## Optimism bias adjustment

Apply a haircut to the P50 benefit before it enters the plan, on top of the booking cap:

| Stage | Haircut on P50 |
|---|---|
| Concept / intake | 40% |
| Pilot approved | 30% |
| MVP in live workflow | 20% |
| Post-scaling, with measured actuals | 0–10%, converging on measured variance |

Both adjustments apply. A Grade C case at pilot stage books `P50 × 0.70 (grade) × 0.70 (stage) = 49%` of its projected benefit. This is intentionally conservative. Cases that survive it are fundable with confidence; cases that do not survive it were never as strong as the slide suggested.
