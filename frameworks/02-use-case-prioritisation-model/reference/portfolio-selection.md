> Component of the [Use Case Prioritisation Model](../README.md) framework.

# From ranking to selection — the constraint problem

A ranked list is not a plan. Selection must respect real constraints, and the binding constraint is almost never money.

Typical binding constraints:

- Scarce specialist capacity (the three people who can actually build this)
- Governance review throughput (the committee meets monthly and can process four assessments)
- Change absorption in the receiving business unit
- Data engineering capacity
- Executive attention

## Selection procedure

1. Declare constraints numerically before looking at the ranking.
2. Remove candidates blocked by unmet dependencies.
3. Reserve the minimum enabler allocation.
4. Select greedily by median composite score, subject to constraints, until the binding constraint is exhausted.
5. Test the shape of the resulting portfolio against the shape targets below.
6. Adjust by explicit exception, minuted, with the reason recorded.

Step 6 matters. Overriding the model is legitimate; overriding it silently is not. The record of exceptions is how the rubric gets improved next cycle.

**Note on optimisation.** Selection under constraints is formally a knapsack problem, and could be solved exactly. The framework deliberately uses greedy selection plus a shape test instead, because the input scores are not precise enough to justify combinatorial optimisation over them. Optimising to three decimal places on Grade D inputs is the same false-precision error in a more sophisticated costume.

## Portfolio shape targets

The selection is tested against shape, not only score. Suggested defaults, to be set locally:

| Dimension | Default target | Rationale |
|---|---|---|
| Number of active use cases | Fewer than instinct suggests | Concentration outperforms breadth; leading organisations run materially fewer than their peers and report better returns |
| Enabler allocation | ≥20% of capacity | Foundations lose every scoring contest without a floor |
| Control-burden mix | No more than one-third of capacity in the highest control tier | High-tier use cases consume governance throughput disproportionately |
| Time-to-value mix | At least one candidate with a credible result inside two quarters | Programme survival depends on demonstrated value before the first budget review |
| Confidence mix | Majority of build-stage capacity at Grade C or better | Otherwise the portfolio is a set of hypotheses |
| Sponsor concentration | No single sponsor holding a majority of capacity | Prevents the portfolio becoming one executive's agenda |

**On concentration.** The instinct in every organisation is to fund more, because refusing a peer's use case is politically expensive. This is the single hardest discipline in the framework and the one most correlated with outcomes.
