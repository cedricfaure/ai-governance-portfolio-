> Component of the [AI Use Case Business Card](../README.md) framework.

# Threshold values (calibration defaults)

These are **starting defaults for a first-time implementation**, to be recalibrated against the organisation's own observed distribution after roughly one year. They are not universal truths, and the card should state which set is in force.

## Gate thresholds

| Metric | Red | Amber | Green |
|---|---|---|---|
| Workflow penetration (by end of MVP) | <30% | 30–60% | >60% |
| Acceptance rate without substantial edit | <50% | 50–70% | >70% |
| L3 operational KPI movement vs baseline | Not statistically distinguishable from zero | Directionally positive, not yet significant | Statistically significant at the pre-declared effect size |
| Risk-adjusted net benefit at scaling gate | Negative | Break-even | Positive and ≥ TCO run rate |
| Baseline Confidence Grade at Build gate | E | D | A–C |

## Cost and planning defaults

| Parameter | Default | Basis |
|---|---|---|
| Annual model maintenance | 15–25% of initial build cost | Established industry guidance |
| Risk reserve | 10–15% of annual AI operating budget | Risk-adjusted ROI literature |
| Technical debt erosion if unserviced | 18–29% of projected return | Cited industry research |
| Talent premium, specialised ML/MLOps roles | 30–50% above comparable software engineering | Cited industry benchmark |
| Early-stage benefit error margin | ±20–30% | Risk-adjusted ROI literature |
| J-curve dip depth | 5–15% below baseline | Must be stated explicitly; a case with no dip must justify why |
| J-curve dip duration | 1–2 quarters | Longer for use cases requiring workflow redesign |
| Realistic payback, focused single use case | 6–18 months | Observed distribution |
| Realistic payback, enterprise transformation | 2–4 years | Observed distribution |

**Sponsor-facing note on payback:** a card projecting payback inside twelve months is claiming a materially better-than-typical outcome. That may be correct — but it should be defended explicitly, not assumed. Very few organisations achieve it.

## Effect-size anchors for sanity-checking projections

Use these to challenge a projection, not to justify one. The correct benefit for any specific use case comes from that use case's baseline, not from a study of a different workflow.

| Setting | Observed effect | Note |
|---|---|---|
| Customer support, ~5,000 agents, staggered rollout | +15% issues resolved per hour | Concentrated in less experienced staff; most experienced saw small speed gain, small quality decline |
| Professional writing tasks, RCT | ~40% time reduction, quality improvement | Bounded, well-specified task |
| Coding, controlled task | ~56% time reduction | Greenfield, task-isolated |
| Experienced developers, mature codebases, RCT | **19% slowdown** | Same developers believed they were ~20% faster |
| Consultants, field experiment | ~40% quality improvement inside model capability | Accuracy declined on tasks outside it |

The last two rows are the important ones. **A projection should explain why this use case resembles the positive rows rather than the negative ones.** Deep expertise in a complex existing system is the strongest predictor of the negative case.
