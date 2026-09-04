> Component of the [Use Case Prioritisation Model](../README.md) framework.

# Worked example — a mid-sized public healthcare authority

**All figures in this example are synthetic and constructed for illustration. This example does not describe any real organisation or engagement.**

This example walks through [`sample-portfolio.csv`](sample-portfolio.csv) — twelve synthetic candidates for a mid-sized public healthcare authority — end to end: the register, the deterministic scores, the stability-tested output, the three bands, a constrained selection, and the shape test. The numbers below are the actual output of `tool/score.py examples/sample-portfolio.csv --iterations 10000 --seed 42`.

## The register

| ID | Name | Enabler? | Depends on |
|---|---|---|---|
| UC01 | AI-Assisted Radiology Triage for Urgent Referrals | | UC02 |
| UC02 | Clinical Data and Imaging Platform | Yes | — |
| UC03 | Ad-hoc Executive Reporting Assistant | Yes | — |
| UC04 | Discharge Summary Drafting Assistant | | UC02 |
| UC05 | Patient Appointment No-show Predictor | | — |
| UC06 | Bed Capacity Forecasting Tool | | — |
| UC07 | General Patient FAQ Chatbot | | — |
| UC08 | AI-Assisted Clinical Coding for Documentation | | UC02 |
| UC09 | Predictive Staffing Model | | UC02 |
| UC10 | Sepsis Early-Warning Model | | — |
| UC11 | Automated Prior-Authorisation Decisioning | | UC12 |
| UC12 | Legacy System Data Extraction Utility | | — |

Built into this register deliberately: two enablers (UC02, foundational, unblocking three others; UC03, low standalone value, no dependants); one high-value, maximum-control-burden candidate (UC01); a pair with near-identical deterministic composites but very different evidence grades (UC05, UC06); a candidate whose Value axis is graded predominantly E (UC10); and a candidate whose sole dependency (UC12) is itself weak (UC11).

## Deterministic scores (the naive point composite)

Before any uncertainty is modelled, the deterministic composite per §1.5 — no dependency adjustment yet — ranks the portfolio as follows:

| Rank | ID | Value | Feasibility | Control | Composite |
|---|---|---|---|---|---|
| 1 | UC04 | 3.60 | 3.55 | 2.25 | 4.83 |
| 2= | UC05 | 3.00 | 3.75 | 2.00 | 4.73 |
| 2= | UC06 | 3.00 | 3.75 | 2.00 | 4.73 |
| 4 | UC02 | 3.10 | 3.05 | 1.75 | 4.63 |
| 5 | UC07 | 2.00 | 4.00 | 1.30 | 4.61 |
| 6 | UC08 | 3.15 | 3.00 | 2.00 | 4.56 |
| 7 | UC09 | 2.80 | 3.00 | 2.00 | 4.42 |
| 8 | UC03 | 1.45 | 3.20 | 1.00 | 4.24 |
| 9 | UC10 | 4.15 | 2.25 | 3.75 | 4.21 |
| 10 | UC01 | 4.20 | 2.80 | 5.00 | 4.02 |
| 11 | UC11 | 2.95 | 2.75 | 3.55 | 3.94 |
| 12 | UC12 | 1.20 | 2.25 | 1.30 | 3.77 |

**Note UC01 already.** Its Value axis (4.20) is the highest in the entire portfolio — higher than UC04's. A value-versus-feasibility model, ignoring Control entirely, would score it at roughly `0.4×4.20 + 0.3×2.80 = 2.52` against UC04's `0.4×3.60 + 0.3×3.55 = 2.51` — essentially tied for first place. Once the Control axis (5.00 — the maximum possible, reflecting high-risk classification under multiple regimes, full technical file and external audit, human approval plus appeal) is subtracted at its 30% weight, UC01 drops to 10th of 12. This is §1.6 in numbers: value and regulatory burden are correlated by construction, and the two-axis view would have sent this candidate straight to the top of the funding queue while understating exactly what it costs to run lawfully.

## Stability-tested output

```
========================================================================================
FRAMEWORK 02 — USE CASE PRIORITISATION MODEL — PORTFOLIO SCORE
========================================================================================
Candidates: 12   Iterations: 10000   Seed: 42
Portfolio Confidence Index (mean evidence grade, A=5..E=1): 3.38
Provisional selection for dependency-adjusted value (§1.8 mechanism 2): base composite >= portfolio median (4.49).

------------------------------------------------------------------------------------------
ID      Name                              Median     P10     P90   P(TopQ)  Conf  Band
------------------------------------------------------------------------------------------
UC02    Clinical Data and Imaging Pla...    5.36    4.95    5.75      1.00   3.8  Robustly prioritised
UC04    Discharge Summary Drafting As...    4.84    4.43    5.22      0.78   3.8  Robustly prioritised
UC05    Patient Appointment No-show P...    4.73    4.37    5.07      0.48   4.5  Contested
UC06    Bed Capacity Forecasting Tool       4.71    4.27    5.13      0.45   2.5  Contested
UC08    AI-Assisted Clinical Coding f...    4.57    4.20    4.91      0.08   3.9  Robustly deprioritised
UC07    General Patient FAQ Chatbot         4.57    4.23    4.91      0.15   3.6  Robustly deprioritised
UC09    Predictive Staffing Model           4.42    4.03    4.80      0.03   3.0  Robustly deprioritised
UC03    Ad-hoc Executive Reporting As...    4.26    3.95    4.59      0.01   2.7  Robustly deprioritised
UC10    Sepsis Early-Warning Model          4.14    3.59    4.67      0.01   2.1  Robustly deprioritised
UC01    AI-Assisted Radiology Triage ...    4.04    3.47    4.56      0.00   4.0  Robustly deprioritised
UC11    Automated Prior-Authorisation...    3.95    3.50    4.37      0.00   3.8  Robustly deprioritised
UC12    Legacy System Data Extraction...    3.81    3.53    4.08      0.00   2.9  Robustly deprioritised
```

## Where naive ranking and stability-tested banding disagree

**UC02.** Naive, pre-adjustment, it ranks 4th of 12 (composite 4.63) — solidly mid-table, the position a data platform with no standalone P&L case typically gets handed in a conventional model. Once the dependency-adjusted value from §1.8 mechanism 2 is applied — UC02 unblocks UC04, which is itself above the provisional selection threshold, so UC02 inherits 30% of UC04's value — and the Monte Carlo test is run, UC02's median composite rises to 5.36 and it is **robustly prioritised** with P(top quartile) = 1.00. A naive rank would have funded the foundation last, if at all, and then been unable to explain why UC01, UC04, UC08 and UC09 were all slow.

**UC05 and UC06.** Identical deterministic composites (4.73). Under stability testing they stay close — UC05 at P(top quartile) 0.48, UC06 at 0.45 — both landing in the **contested** band rather than splitting apart. This is itself the point: two candidates that look identical on a point estimate, one built on Grade A/B evidence and the other on Grade C/D, are not actually distinguishable enough to justify a confident order between them, and the model correctly declines to manufacture one. A naive rank would have had to put one above the other; the honest answer here is "we cannot currently tell, and here is why."

## The three bands

**Robustly prioritised (2):** UC02, UC04.

**Contested (2):** UC05, UC06 — a genuine judgement call for the panel, not a model failure.

**Robustly deprioritised (8):** UC08, UC07, UC09, UC03, UC10, UC01, UC11, UC12.

**Validation warnings raised:**

- UC03 (enabler) scores below the portfolio median composite — check the minimum enabler allocation policy before letting the score alone decide.
- UC03 and UC10 both have a Value axis graded predominantly D–E — per §1.7 rule 1, neither can be selected for build; each may only be selected for a discovery sprint whose deliverable is better evidence. For UC10 this is a deliberate design feature of this example: a genuinely promising sepsis early-warning concept, scored high on value but backed only by vendor claims (Grade E) — exactly the case the rule exists to catch before it is funded as if it were evidenced.
- UC11 depends on UC12, which is Robustly deprioritised, not Robustly prioritised — an unmet dependency. UC11 cannot be sequenced ahead of it regardless of its own score.

## Constrained selection

Declared constraint for this cycle: **8 units of specialist build capacity** (the binding constraint, per §1.10 — not money).

1. **Constraint declared:** 8 units.
2. **Blocked by unmet dependency:** UC11 is removed from this cycle's selection — its dependency, UC12, is not itself prioritised.
3. **Minimum enabler allocation reserved:** ≥20% of 8 units = at least ~1.6 units. UC02 (4 units) already clears this on its own merit, at the top of the ranking.
4. **Greedy selection by median composite, respecting dependency order, until capacity is exhausted:**

| Order | ID | Median | Capacity | Running total |
|---|---|---|---|---|
| 1 | UC02 | 5.36 | 4 | 4 |
| 2 | UC04 | 4.84 | 2 | 6 |
| 3 | UC05 | 4.73 | 1 | 7 |
| 4 | UC06 | 4.71 | 1 | 8 — capacity exhausted |

UC08, UC07, UC09, UC03, UC10, UC01 and UC12 are not funded this cycle on the model's output alone.

5. **Shape test** against the §1.11 defaults:

| Dimension | Target | This selection |
|---|---|---|
| Number of active use cases | Fewer than instinct suggests | 4 — meets it |
| Enabler allocation | ≥20% of capacity | UC02 alone is 4/8 = 50% — meets it |
| Control-burden mix | ≤1/3 of capacity in the highest control tier | 0% — UC01, the highest-burden candidate, is not selected — meets it |
| Time-to-value mix | ≥1 candidate with a credible result inside two quarters | UC04's Business Card projects a result inside two quarters — meets it |
| Confidence mix | Majority of build capacity at Grade C or better | UC02, UC04, UC05 (7 of 8 units) are C-or-better on balance; only UC06 (1 unit) is weaker — meets it |
| Sponsor concentration | No single sponsor holding a majority | Four different sponsors across the four selected candidates — meets it |

6. **Exception, taken deliberately and minuted:** the panel adds **UC12** (1 unit) against the model's own output — it is Robustly deprioritised — specifically because the Director of Payer Relations has flagged UC11 (Automated Prior-Authorisation Decisioning) as addressing a near-term regulatory commitment, and UC11 cannot proceed while its sole dependency remains unfunded. The panel records the reasoning: *funding the low-scoring dependency is judged cheaper than leaving a strategically necessary, higher-scoring dependant permanently blocked; the resulting one-unit overrun against the declared 8-unit capacity is accepted for this cycle and will be reconciled at the next capacity review.* This is logged in the exception register per §1.12 rule 6, owner: AI Governance Board Chair.

Total funded this cycle: UC02, UC04, UC05, UC06, UC12 — 9 units against an 8-unit declared constraint, by minuted exception. UC11 remains queued for the following cycle, contingent on UC12's delivery.

## A note on the currency question this example is allowed to answer

Framework 02 deliberately scores Cost of Control on a relative 1–5 scale rather than in currency, for the reasons set out in [cost-of-control-rationale.md](../reference/cost-of-control-rationale.md) — published compliance-cost estimates diverge by more than an order of magnitude and are not reconcilable into a defensible unit cost. This worked example is the one place in the framework where a synthetic currency figure is permitted, precisely to show what that discipline is protecting against: after its first two high-tier systems, this synthetic authority's own retrospective figure for UC01-class control overhead — technical file, external audit, oversight staffing and appeal handling, combined — came to approximately **AED 1.2 million in year one**, against an initial estimate, made at intake using an external benchmark, of AED 180,000. Neither number belongs in the general framework text; the discipline of scoring the axis relatively, and calibrating it locally once real data exists, is what the general framework text says instead.

## What this example is designed to show

- How the Control axis corrects a structural bias, not a random error: UC01 has the highest Value score in the portfolio and the maximum possible Control score, and a two-axis model would have funded it first.
- How dependency-adjusted value stops an enabler (UC02) losing every cycle to more visible candidates with their own sponsors, and how that changes its band, not just its score.
- How two candidates with identical deterministic composites (UC05, UC06) can still be told apart by their evidence grade once uncertainty is modelled — and how the model is honest about when it cannot tell them apart at all (both land Contested).
- How the discovery-only flag catches a genuinely exciting but under-evidenced candidate (UC10) before it is funded as if it had been.
- How an unmet dependency (UC11 → UC12) blocks sequencing regardless of the dependent candidate's own score, and how a panel can still choose to override that with a minuted, reasoned exception rather than silently working around the model.
- That a constrained, shape-tested selection of four to five candidates — not a ranked list of twelve — is the actual deliverable of this framework.
