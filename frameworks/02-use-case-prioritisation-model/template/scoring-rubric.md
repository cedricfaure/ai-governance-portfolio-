<!--
Use Case Prioritisation Model — scoring rubric.
This is the working document a panel prints and uses in the room: it is
self-contained and does not require the reference/ files to be scored.
See ../README.md for the framework this rubric belongs to.
-->

# Scoring rubric

## Panel composition

Minimum panel: business sponsor (presents, does not score), process owner, data lead, technology lead, risk and compliance.

**The sponsor presents; the panel scores.** This is non-negotiable, and is the single most effective anti-gaming control available.

Every score above 3 requires stated evidence, recorded against the criterion. No evidence, score capped at 3. Record an evidence grade (A–E, same scheme as the Business Card baseline grades) alongside every score:

| Grade | Evidence behind the score |
|---|---|
| A | System-derived data or completed assessment |
| B | Process-mined or documented analysis |
| C | Structured study or formal review |
| D | Structured expert elicitation, ≥3 independent assessors, dispersion recorded |
| E | Single assertion, vendor claim, or external benchmark only |

Evidence grade is scored by the panel, not the sponsor.

Five-point scale, anchored. Anchors are mandatory: an unanchored 1–5 scale is an opinion poll.

---

## Axis 1 — Value (weight 40%)

### Risk-adjusted net benefit — 35% of axis (using the capped figure from the Business Card)

| Score | Anchor |
|---|---|
| 1 | Negative or indistinguishable from zero |
| 2 | Positive but below the portfolio's median candidate |
| 3 | Around the portfolio median |
| 4 | Materially above median; payback within the organisation's stated horizon |
| 5 | Top decile of the portfolio; payback comfortably inside horizon at P10 |

**Score:** ___  **Evidence grade:** ___  **Evidence:**

### Strategic fit — 25% of axis

| Score | Anchor |
|---|---|
| 1 | No mapping to a stated objective |
| 2 | Loosely related to a stated objective |
| 3 | Supports a stated objective |
| 4 | Directly advances a named objective with an accountable executive |
| 5 | Named in the current strategic plan as a required capability |

**Score:** ___  **Evidence grade:** ___  **Evidence:**

### Non-monetisable / mission value — 20% of axis

| Score | Anchor |
|---|---|
| 1 | None claimed, or Tier 3 only |
| 2 | Tier 2 claimed without a baseline (treat as Tier 3) |
| 3 | One Tier 2 benefit with baseline and target |
| 4 | Multiple Tier 2 benefits with baselines, or one central to the organisation's mandate |
| 5 | Directly delivers a statutory or mandated outcome |

**Score:** ___  **Evidence grade:** ___  **Evidence:**

### Reusability — 20% of axis

| Score | Anchor |
|---|---|
| 1 | Wholly bespoke; creates nothing reusable |
| 2 | Minor reusable components |
| 3 | Creates one reusable asset (dataset, pipeline, evaluation harness, control set) |
| 4 | Creates reusable assets that two or more identified candidates depend on |
| 5 | Foundational: multiple downstream candidates are blocked without it |

**Score:** ___  **Evidence grade:** ___  **Evidence:**

---

## Axis 2 — Feasibility (weight 30%)

### Data readiness — 30% of axis

| Score | Anchor |
|---|---|
| 1 | Data does not exist or cannot be lawfully used |
| 2 | Exists but not accessible; quality unknown |
| 3 | Accessible; quality partially understood; remediation needed |
| 4 | Accessible, profiled, quality known and adequate |
| 5 | Accessible, governed, quality assured, already used in production |

**Score:** ___  **Evidence grade:** ___  **Evidence:**

### Technical complexity — 20% of axis (higher score = less complex)

| Score | Anchor |
|---|---|
| 1 | Depends on unproven capability or a research outcome |
| 2 | Novel to the organisation; extensive integration |
| 3 | Established pattern; moderate integration |
| 4 | Established pattern; limited integration; existing platform |
| 5 | Configuration of an existing deployed capability |

**Score:** ___  **Evidence grade:** ___  **Evidence:**

### Workflow change burden — 25% of axis (higher score = less burden)

**Rule:** this criterion is scored inversely to the temptation. A use case requiring no workflow change is easy — and, on the evidence, likely to deliver little. Score the burden honestly as a cost, but read a near-zero burden (a score of 5) as a warning about Axis 1, not a strength. Overlaying AI on an unchanged process is the dominant failure pattern.

| Score | Anchor |
|---|---|
| 1 | Redesign across multiple functions with contested ownership |
| 2 | Significant redesign within one function |
| 3 | Moderate change; roles adjust |
| 4 | Contained change; existing roles absorb it |
| 5 | Minimal change — and therefore check Axis 1 for marginal value |

**Score:** ___  **Evidence grade:** ___  **Evidence:**

### Sponsorship and capacity — 25% of axis

| Score | Anchor |
|---|---|
| 1 | No named sponsor, or required people are committed elsewhere |
| 2 | Sponsor named but without decision authority |
| 3 | Sponsor with authority; capacity uncertain |
| 4 | Sponsor with authority; capacity confirmed for the first gate |
| 5 | Sponsor with authority and budget; capacity confirmed through scaling |

**Score:** ___  **Evidence grade:** ___  **Evidence:**

---

## Axis 3 — Cost of Control (weight 30%, scored as a penalty — subtracted, not added)

### Regulatory classification burden — 30% of axis

| Score | Anchor |
|---|---|
| 1 | Out of scope of any applicable regime, or minimal-risk with no specific obligations |
| 2 | Transparency obligations only |
| 3 | Enhanced obligations short of the high-risk tier, or high-risk with a mature control set already in place |
| 4 | High-risk tier under one applicable regime; new obligations |
| 5 | High-risk under multiple regimes, or requiring third-party conformity assessment, or unresolved classification |

**Score:** ___  **Evidence grade:** ___  **Evidence:**

### Oversight operating cost — 25% of axis

| Score | Anchor |
|---|---|
| 1 | No human in the loop required |
| 2 | Human on the loop, exception-based |
| 3 | Sampled human review |
| 4 | Human approval on every consequential output |
| 5 | Human approval plus a contestability and appeal process |

**Score:** ___  **Evidence grade:** ___  **Evidence:**

### Assurance and evidence burden — 25% of axis

| Score | Anchor |
|---|---|
| 1 | Standard change documentation |
| 2 | Model documentation and basic monitoring |
| 3 | Impact assessment plus ongoing monitoring |
| 4 | Full technical file, logging retention, post-market monitoring |
| 5 | All of the above plus external audit or certification |

**Score:** ___  **Evidence grade:** ___  **Evidence:**

### Residual risk exposure — 20% of axis

| Score | Anchor |
|---|---|
| 1 | Negative risk delta immaterial after controls |
| 2 | Small residual, well characterised |
| 3 | Moderate residual; loss expectancy estimable |
| 4 | Material residual; affects people's access to services, money, or opportunity |
| 5 | Material residual with poorly characterised loss distribution |

**Score:** ___  **Evidence grade:** ___  **Evidence:**

---

## Composite score

```
Priority Score = (0.40 × Value) + (0.30 × Feasibility) − (0.30 × Control) + 3.0
```

The +3.0 constant keeps the score positive and readable; it is a presentation device and carries no meaning.

Do not read this composite as a rank on its own — see [rank-stability.md](../reference/rank-stability.md) for the stability test that must be run before any selection decision is made.
