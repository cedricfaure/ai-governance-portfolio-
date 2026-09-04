> Component of the [Use Case Prioritisation Model](../README.md) framework.

# Why Cost of Control is a separate axis — the structural bias argument

This section is the intellectual core of the framework. It must be reproduced in full.

Regulatory risk tiers are assigned on the basis of consequence to people. Systems that influence access to employment, credit, education, essential public services, healthcare, or law enforcement outcomes attract the heaviest obligations — precisely because the decisions they touch matter.

But those are the same decisions that carry the most organisational value. High-consequence decisions are high-volume, high-cost, and high-stakes; automating or augmenting them is where the money is.

The two facts are the same fact. Value and regulatory burden are positively correlated by construction, not by coincidence.

The consequence: a value-versus-feasibility model systematically over-ranks exactly the use cases whose true cost it omits. The error is not random noise that averages out across a portfolio; it is a directional bias concentrated in the candidates the model recommends most strongly. An organisation using a two-axis model will reliably approve its highest-burden use cases while believing it has costed them.

Making control cost a separate, subtracted axis does three things:

1. It corrects the bias at the point of selection rather than at pre-deployment, when the money is already spent.
2. It makes the trade-off visible and arguable rather than implicit — a sponsor can now say "the value survives the burden" and be checked.
3. It reframes governance from a brake into a priced input. A high-burden use case is not forbidden; it must simply clear a higher bar, which is exactly what a rational investor would require.

## On costing this axis in currency

The framework deliberately scores control cost on a relative 1–5 scale rather than in currency. Published estimates of compliance cost for a single high-risk AI system diverge by more than an order of magnitude — from roughly €10,000 for self-assessed conformity, to €193,000–330,000 for quality management system establishment with substantial annual maintenance, to independent analyses citing $8–15M initial programme cost at large enterprises. These figures measure different things (per-system versus programme-wide, provider versus deployer, marginal versus fully-loaded) and are not reconcilable into a defensible unit cost.

Anyone publishing a single per-system compliance figure is either scoping something narrower than they state or guessing. The honest treatment is a relative burden tier, calibrated against the organisation's own observed cost after its first two or three high-tier systems. Until that internal data exists, use the tier; do not manufacture a number.
