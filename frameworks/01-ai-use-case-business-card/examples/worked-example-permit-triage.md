> Component of the [AI Use Case Business Card](../README.md) framework.

# Worked example — construction permit triage

**All figures in this example are synthetic and constructed for illustration. This example does not describe any real organisation or engagement.**

---

## Block 1 — Identity & accountability

**Use case ID:** UC-0142
**Name:** AI-assisted first-pass triage for construction permit applications
**Business sponsor:** [Named individual — synthetic]
**Process owner:** Head of Permitting Operations
**Technical owner:** [Named individual — synthetic]
**Risk owner:** Head of Regulatory Risk
**Date raised:** 2026-02-03
**Version:** 1.2
**Current gate:** 1 Pilot — completed; this card supports the Gate 2 (MVP) investment decision.

## Block 2 — Problem & counterfactual

**Decision or task being changed:** First-pass review and categorisation of inbound construction permit applications (routine / needs inspection / high-risk), currently performed entirely by permitting officers.
**Who currently performs it:** Permitting officers (14 FTE)
**Volume (per period):** ~40,000 applications per year
**Counterfactual:** Application volume is forecast to grow 12% over the next two years on current planning trends. Without intervention, the permitting service has a signed plan to recruit two additional officers to hold response times steady — this cost genuinely arrives if nothing changes, and is the basis for the avoided-hire benefit below.

## Block 3 — Workflow delta

**Process today:** An officer opens each application, reviews the submitted documents, manually sorts it into routine, needs-inspection, or high-risk, and then completes the full assessment and issues the determination — all performed sequentially by the same officer.

**Process after:** On receipt, an AI triage model extracts key document fields and proposes a routing category for each application. The officer reviews the proposed category, corrects it where wrong, and then completes the assessment and issues the determination exactly as before. Applications the model flags as high-risk are additionally routed to a senior reviewer for a second check before the officer's determination.

**Steps removed:** Manual first-pass document sorting and categorisation.

**New steps introduced:** AI-output verification (the officer confirms or overrides the proposed category); a senior-reviewer second check on AI-flagged high-risk applications.

**Human decision point after the change:** The officer retains the full determination decision on every application. The AI changes how the application is sorted before review — not who decides the outcome.

## Block 4 — Value hypothesis

| Shape | Description | Unit | AED value (P50) | Baseline source | Realisation path |
|---|---|---|---|---|---|
| B2 | Labour time compression on first-pass sorting, redirected to avoid planned headcount growth | AED, fully loaded avoided-hire cost | AED 140,000 / year (raw, pre-cap) | Time-motion study (Grade C) | Avoided two planned hires budgeted for the next financial year |
| B7 | Faster time to first response for applicants (non-monetisable, Tier 2) | Median days to first response | Baseline 11 days → target 6 days | Time-motion study, same sample | Presented alongside the financial case, not inside it |

**Note on B2:** the raw benefit is not "hours saved × rate". It is booked at the value of the two hires the service will not now need to make, per the counterfactual in Block 2. Residual freed time beyond the avoided hires is not claimed as a financial benefit.

## Block 5 — KPI ladder

| Layer | KPI | Owner | Baseline | Target | Threshold | Measurement method |
|---|---|---|---|---|---|---|
| L5 Technical | Triage classification error rate | Technical owner | n/a (new system) | <8% misclassification vs senior-reviewer adjudication | Amber >8%, Red >15% | Weekly sample audit of 200 applications |
| L4 Adoption | Workflow penetration | Process owner | 0% | >60% of eligible applications triaged with AI support | Red <30%, Amber 30–60% | System log, eligible applications frozen at definition |
| L4 Adoption | Acceptance rate (category confirmed with no override) | Process owner | n/a | >70% | Red <50%, Amber 50–70% | System log |
| L3 Operational | Median cycle time, receipt to first response | Process owner | 11 working days | 6 working days | Not distinguishable from baseline = Red | Staggered-rollout comparison, treated vs not-yet-treated sites |
| L3 Operational | Cost per case (labour + system + rework) | Process owner | AED 38 / case | AED 29 / case | Directionally positive but not significant = Amber | Finance system + rework log |
| L2 Strategic | Applicant complaint/appeal rate on triage outcome | Head of Permitting Operations | 1.8% | ≤1.8% (no degradation) | Increase >0.5pp = Red | Complaints register |
| L1 Financial | Risk-adjusted net benefit vs TCO | Finance | n/a | Positive by Gate 3 | Negative at Gate 3 = Red | This card, Block 7 |

## Block 6 — Baseline & attribution

**Baseline Confidence Grade:** C — three-week time-motion study, statistically sampled across officers, shifts and application types.
**Attribution design:** Staggered rollout — deployment sequenced across four permitting offices over two quarters; early sites compared against not-yet-deployed sites.
**Optimism bias adjustment applied:** Pilot approved stage → 30% haircut.
**Combined booking factor:** Grade C cap (70%) × Pilot-stage haircut (70%) = **49% of P50** enters the financial plan below.

## Block 7 — Cost & TCO

| Component | AED |
|---|---|
| Build (one-off) | 90,000 |
| Run (annual) | 40,000 |
| Governance (annual) | 10,000 |
| Reserve (annual, ~12% of run + governance) | 6,000 |
| **Annual opex (Run + Governance + Reserve)** | **56,000** |
| **Year 1 Total TCO (Build + annual opex)** | **146,000** |

**Gross benefit, raw P10 / P50 / P90 (annual):** AED 70,000 / AED 140,000 / AED 200,000
**Gross benefit, booked at 49% (annual, enters the plan):** AED 34,300 / AED 68,600 / AED 98,000

**Risk delta (annual):** −AED 8,000 / −AED 3,000 / −AED 800
*(See Block 8 — this is a net risk **increase**, not a reduction, and is subtracted accordingly.)*

**Risk-adjusted net benefit, Year 1 (booked benefit + risk delta − Year 1 TCO):**
P10 −AED 119,700 · P50 −AED 80,400 · P90 −AED 48,800

**Risk-adjusted net benefit, ongoing annual from Year 2 (booked benefit + risk delta − annual opex, Build already spent):**
P10 −AED 29,700 · P50 +AED 9,600 · P90 +AED 41,200

**Risk-adjusted ROI %, ongoing annual (net benefit ÷ annual opex × 100):**
P10 −53% · P50 +17% · P90 +74%

**Payback period (from go-live, including Build recoupment):**
- **P10:** not achieved within the three-year appraisal window at current conservative booking. This is the marginal case: it does not currently justify Build on its own financial merits, and is carried forward on the strength of the P50/P90 range plus the Tier 2 case, with the kill criteria in Block 10 as the safeguard.
- **P50:** approximately 9 years at current Pilot-stage booking. This is a function of the deliberate 49% haircut, not a claim about real expected performance — it is expected to shorten materially once Grade C is upgraded to B or A and the stage haircut falls to 0–10% at the Scale gate, when actuals replace projections.
- **P90:** approximately 26 months.

## Block 8 — Risk & governance

**Risk classification:** Limited-risk automated decision support (human retains the determination); classified against the organisation's internal AI risk tiering and reviewed for applicable public-sector automated-decision obligations.
**Provider or deployer role:** Deployer (model developed by an internal team using a licensed third-party document-extraction component).
**Human oversight model:** Human in the loop — the officer reviews the AI-proposed triage category before acting on it, and independently makes the full determination on every application. High-risk flags receive an additional senior-reviewer check.
**Affected persons:** Permit applicants, including small contractors and individual homeowners who may have less capacity to navigate an appeal.
**Contestability:** Existing appeal route for permit determinations is unchanged; applicants are not informed which category was AI-proposed, only the outcome, consistent with legal advice that the officer's determination — not the triage step — is the decision of legal effect.
**Data provenance and lawful basis:** Application documents submitted directly by applicants under the existing statutory permitting process; no additional personal data collected for the triage model.
**Risk delta scenarios carried into Block 7:**
- *Misrouted high-risk application proceeds as routine without required inspection.* Single Loss Expectancy AED 150,000 (remediation, re-inspection, reputational cost). Annualised Rate of Occurrence: 0.05 today (rare officer error) → estimated 0.08 during the first year of AI-assisted triage, reflecting automation-complacency risk before the verification habit is established. ALE before AED 7,500; ALE after AED 12,000. **Risk delta: −AED 4,500 (a net risk increase)**, before the stage-appropriate adjustment shown in Block 7.
**Impact assessment required:** Yes — internal automated-decision-support impact assessment completed prior to Gate 1; reference ADS-IA-0142.

## Block 9 — Gates & cadence

| Gate | Decision | Evidence | Decision-maker | Date |
|---|---|---|---|---|
| 0 Intake | Go | Card completed to Block 4; counterfactual confirmed against signed recruitment plan; baseline grade declared as target C | Head of Permitting Operations | 2026-02-10 |
| 1 Pilot | Go | Grade C baseline established (three-week time-motion study); staggered-rollout attribution design locked; L5 error rate within guardrail on held-out sample | AI Governance Board | 2026-04-28 |
| 2 MVP | Pending | This card is the supporting evidence for this decision | AI Governance Board | Scheduled 2026-09 |
| 3 Scale | Pending | — | Investment Committee | — |
| 4 Sustain | Pending | — | AI Governance Board | — |

## Block 10 — Kill criteria

- Workflow penetration below 30% at Gate 2 despite a completed enablement plan → the automated triage step is paused and the workflow reverts to fully manual sorting pending redesign.
- The misrouted-high-risk escalation rate exceeds 1 in 500 triaged applications in any rolling quarter (breaching the Block 8 risk-delta assumption) → the triage model is suspended pending root-cause review, regardless of other KPI performance.
- Risk-adjusted net benefit remains negative at Gate 3 under a Grade B baseline or better, with no credible path to positive within 12 months → the use case is decommissioned.
- Median days-to-first-response has not improved from the 11-day baseline by Gate 3 → the programme is stopped regardless of L5/L4 technical performance, since the stated Tier 2 objective would not have been met.

## Version history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-02-03 | Initial card at intake |
| 1.1 | 2026-04-28 | Updated following Gate 1 with confirmed Grade C baseline |
| 1.2 | 2026-06-15 | Refreshed KPI table ahead of Gate 2 submission |

---

### What this example is designed to show

- How the booking cap and stage haircut combine mechanically (0.70 × 0.70 = 49%) to produce a conservative number that enters the plan — and why that number can look weak even when the underlying opportunity is real.
- How an hour saved becomes a defensible financial benefit only when tied to a stated realisation path (here, two avoided hires against a signed recruitment plan), not simply hours multiplied by a rate.
- How a Tier 2 non-monetisable benefit (days to first response) sits alongside the financial case rather than inside it, and can still anchor a kill criterion in its own right.
- How a risk delta can be **negative** — a net risk increase, not a reduction — and must be subtracted from the benefit rather than ignored because it is inconvenient.
- Why a marginal P10 case is not a reason to hide the number: it is the honest range the sponsor is being asked to accept, with the kill criteria in Block 10 as the actual safeguard rather than a rosier point estimate.
- How the human-in-the-loop oversight claim in Block 8 is consistent with the workflow delta in Block 3 — the officer is removed from sorting, not from deciding — which is the specific consistency check the framework asks reviewers to make.
