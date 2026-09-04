> Component of the [Use Case Prioritisation Model](../README.md) framework.

# Rank stability — the Monte Carlo test

**The problem.** Multi-criteria scoring models are vulnerable to rank reversal: the relative order of two alternatives can change when an unrelated alternative is added to or removed from the candidate set. This is a violation of independence of irrelevant alternatives, demonstrated in the Analytic Hierarchy Process in 1983 and argued over ever since. An AI use case portfolio has candidates added and dropped every cycle. Any hard ranking it produces is partly an artefact of which candidates happened to be in the room.

Combined with uncertain scores and arbitrary-to-two-decimal-places weights, a ranked list from this class of model conveys far more precision than it holds.

**The treatment.** Do not publish a rank. Publish a stability-tested band.

## Procedure

1. Treat each criterion score as a distribution rather than a point. Width by evidence grade: A = ±0.25, B = ±0.4, C = ±0.6, D = ±0.9, E = ±1.3 (truncated to the 1–5 scale).
2. Treat axis weights as uncertain: Dirichlet-distributed around the declared weights, concentration set so that weights vary by roughly ±5 percentage points.
3. Run ≥10,000 iterations. In each, sample scores and weights, compute the composite, and record each candidate's rank.
4. Report, per candidate: median composite, 10th–90th percentile composite, and P(top quartile) — the proportion of iterations in which it lands in the top quartile of the portfolio.

## Interpretation rules

- **P(top quartile) > 0.75** → robustly prioritised. Fund it.
- **0.25 – 0.75** → genuinely contested. The model cannot separate these; the decision is a judgement call and should be made and minuted as one.
- **< 0.25** → robustly deprioritised. Say no, and say why.

This is the framework's central honesty claim. A model that outputs "ranked 4th" when the underlying evidence supports "somewhere between 2nd and 11th" is not being rigorous; it is laundering uncertainty into false authority. Banding is less satisfying and more true. Expect resistance from stakeholders who wanted a number, and hold the line — the credibility of the whole process depends on it.
