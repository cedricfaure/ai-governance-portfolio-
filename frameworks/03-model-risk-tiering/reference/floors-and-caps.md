> Component of the [Model Risk Tiering Scheme](../README.md) framework.

# Floors and caps — the non-compensatory layer

**The problem with additive scoring.** A weighted average lets a high score on one dimension be offset by low scores elsewhere. For risk classification this is not a rounding issue; it is a category error. A system that can cause irreversible harm to a vulnerable person does not become safe because it is transparent, cheap to run and built in-house. Compensation is invalid whenever a single dimension is independently sufficient to warrant control.

Floors and caps make the scheme non-compensatory where it must be, and proportionate everywhere else. They are the most important mechanism in the framework.

## Floor rules — these raise the tier and cannot be traded away

| ID | Condition | Effect |
|---|---|---|
| F0 | The use falls within a practice prohibited under an applicable regime, or breaches a declared organisational red line | T0 — refuse |
| F1 | Output determines or materially influences access to employment, credit, education, housing, healthcare, social benefits, or an essential public or private service | Minimum T3 |
| F2 | System can initiate an irreversible or externally visible action without per-instance human confirmation (D4 = 5) | Minimum T3 |
| F3 | Decision subjects include children or persons in a legally recognised position of vulnerability or dependence | Minimum T3 |
| F4 | System is classified as high-risk, or equivalent, under any applicable external regime | Minimum T3 |
| F5 | Failure could result in physical harm, or affects safety-relevant functions or critical infrastructure | Minimum T4 |
| F6 | Output determines a regulatory, statutory, prudential or capital outcome (D6 = 5) | Minimum T3 |
| F7 | Special-category data with unresolved lawful basis or undocumented provenance (D8 = 5) | Minimum T3 |
| F8 | D4 ≥ 4 and D9 ≥ 4 — meaningful autonomy combined with behaviour that changes without a release | Minimum T3 |
| F9 | D3 = 5 and D2 ≥ 4 — irreversible effect on a large or vulnerable population | Minimum T4 |
| F10 | No accountable named owner, or no identified process owner | Minimum T3 until remedied; may not enter production |

F10 is not a risk about the system. It is a risk about the organisation, and it is placed here deliberately: an unowned system cannot be governed at any tier, and the fastest way to get an owner named is to make the absence expensive.

F8 is the agentic gap rule. It captures precisely the combination that the revised MRM guidance does not reach: a system that acts, and whose behaviour drifts without anything a change-control process would notice.

## Cap rules — these lower the tier, and every condition must hold

| ID | All conditions required | Effect |
|---|---|---|
| C1 | No personal data · no external effect · fully reversible · human decides independently (D4 ≤ 2, D5 ≤ 2) · no regulatory purpose | Maximum T2 |
| C2 | Sandbox or evaluation environment · no production data · no production output · time-boxed with a declared expiry | Maximum T1, expires with the time box |

**Caps never override floors.** Where a cap and a floor conflict, the floor wins, always, without exception and without a discretionary override. This precedence rule must be enforced in code, not left to the assessor.

## Resolution order

Deterministic, in this exact sequence:

1. Compute the provisional tier from the score.
2. Evaluate F0. If it fires: T0, stop. No further processing.
3. Evaluate all remaining floors. Take the highest floor triggered.
4. Inherent Tier = max(provisional tier, highest floor).
5. Evaluate caps. Apply only if the resulting tier would remain at or above every triggered floor.
6. Record the complete trail: score, band, every rule evaluated, every rule fired, and the final assignment.

Step 6 is not optional. A tier without its rule trail is an assertion; a tier with one is a decision that can be reviewed, challenged and re-run.
