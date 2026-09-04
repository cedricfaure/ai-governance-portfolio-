> Component of the [Model Risk Tiering Scheme](../README.md) framework.

# Worked examples

**All examples are synthetic and constructed for illustration. They do not describe any real organisation, engagement or system.**

Each example below is walked through with the actual output of `tool/tier.py` run against the corresponding file in this directory, on the rule set as published (version 1.0.0).

## Example 1 — Internal Meeting Summariser

`01-internal-summariser.yaml`. A third-party-foundation-model summariser posted to the meeting organiser only; no decision or action follows automatically. Low scores across all ten dimensions, and every C1 condition (no personal data, no external effect, fully reversible, human decides independently, no regulatory purpose) is met.

```
$ python3 tool/tier.py examples/01-internal-summariser.yaml --rules rules
Family scores — A(Impact)=1.300 B(Agency)=1.300 C(Uncertainty)=1.750
Raw score = 1.412 -> Inherent Risk Percentage = 10.3% -> provisional tier T1
No floors fired.
C1 FIRED — ... Cap condition(s) matched but did not lower the tier (already at or below the cap).
FINAL INHERENT TIER: T1
RESIDUAL TIER: T1
```

**What this shows:** the scheme is proportionate and does not over-govern. The score alone already lands at T1; C1 fires but has nothing left to do, because a low-consequence, fully reversible, non-personal-data use case doesn't need the cap to reach the right answer — it demonstrates the cap working correctly rather than working hard.

## Example 2 — Benefit Eligibility Triage Engine (the flagship example)

`02-benefit-eligibility-triage.yaml`. A **deterministic rules engine** — no machine learning at all — that triages benefit applications. It is transparent (D7=1), fully in-house (D10=1) and behaviourally static (D9=1). Under the revised MRM guidance's narrowed "model" definition it is explicitly out of scope (a deterministic rule-based process with no statistical or economic theory underpinning it). It is equally out of scope of AI-specific regulation, for the same reason: it isn't AI.

```
$ python3 tool/tier.py examples/02-benefit-eligibility-triage.yaml --rules rules --obligations
Family scores — A(Impact)=3.700 B(Agency)=2.600 C(Uncertainty)=1.500
Raw score = 2.765 -> Inherent Risk Percentage = 44.1% -> provisional tier T2
F1 FIRED — Output determines or materially influences access to ... social benefits ...
F3 FIRED — Decision subjects include children or persons in a legally recognised
           position of vulnerability or dependence
Floors fired: ['F1', 'F3']. Highest floor effect: T3.
Inherent Tier (pre-cap) = max(provisional T2, floors) = T3
FINAL INHERENT TIER: T3
RESIDUAL TIER: T3
```

**What this shows:** a score-only scheme would have rated this T2 at best — moderate, on the numbers. It is a system that no version of the revised MRM guidance reaches, and that most AI-specific regulation would never even look at, because it contains no AI. Yet it decides who gets a benefit. This is exactly what floors are for, and exactly the gap described in [the SR 26-2 gap](../reference/sr26-2-gap.md): a system invisible to both external regimes, correctly caught by the internal scheme because scope here is anchored on consequence, not construction.

## Example 3 — Agentic Procurement Assistant

`03-agentic-procurement-assistant.yaml`. Drafts and issues purchase orders below a delegated threshold, without per-instance human confirmation, built on a third-party foundation model. D4=5 (initiates externally visible action alone), D9=4 (behaviour can change on a supplier-side model update). A mitigation is claimed — a purchase-order value cap and supplier allowlist — but its evidence is nearly a year old against a 30-day T3 monitoring cadence.

```
$ python3 tool/tier.py examples/03-agentic-procurement-assistant.yaml --rules rules
Family scores — A(Impact)=2.700 B(Agency)=4.100 C(Uncertainty)=3.250
Raw score = 3.327 -> Inherent Risk Percentage = 58.2% -> provisional tier T3
F2 FIRED — System can initiate an irreversible or externally visible action
           without per-instance human confirmation (D4 = 5)
F8 FIRED — D4 >= 4 and D9 >= 4 — meaningful autonomy combined with behaviour
           that changes without a release
Floors fired: ['F2', 'F8']. Highest floor effect: T3.
FINAL INHERENT TIER: T3
Mitigation 'Purchase order value cap and pre-approved supplier allowlist,
enforced in the tool-call layer' evidence is 307 days old, exceeding the T3
cadence of 30 days. LAPSED — no credit.
RESIDUAL TIER: T3
```

**What this shows:** F8, the agentic gap rule, catches precisely what the revised MRM guidance does not reach — meaningful autonomy (D4) combined with behaviour that can drift without anything a code-release-keyed change process would ever see (D9). And the lapse mechanic is automatic: a control that was real once but hasn't been checked in ten months earns nothing, without anyone having to notice the evidence went stale. Residual Tier stays at the Inherent Tier — T3 — because there is currently no valid, evidenced control to credit.

## Example 4 — Shared Document Embedding Pipeline

`04-shared-embedding-pipeline.yaml`. Infrastructure with no decision-making role of its own — converts documents to vector embeddings for other systems to consume. Scores T1 on every dimension, standalone. Three other systems in this directory (`04a-credit-line-adjuster.yaml`, `04b-claims-severity-scorer.yaml`, `04c-fraud-risk-flagger.yaml` — synthetic supporting fixtures for this example, each independently T3 via F1) declare it as a dependency.

```
$ python3 tool/tier.py examples/04-shared-embedding-pipeline.yaml --rules rules
Family scores — A(Impact)=1.000 B(Agency)=1.300 C(Uncertainty)=2.250
Raw score = 1.417 -> Inherent Risk Percentage = 10.4% -> provisional tier T1
No floors fired.
Common-mode dependency (§1.11 rule 5): 3 dependants at T3 or higher share this
component (SYS-CREDIT-ADJ=T3, SYS-CLAIMS-SEV=T3, SYS-FRAUD-FLAG=T3). Tiered
at the maximum of its dependants: T3.
FINAL INHERENT TIER: T3
RESIDUAL TIER: T3
```

**What this shows:** aggregate risk, structurally. Standalone tiering would sign this system off at T1 forever — nothing about the pipeline itself changed. It is rule 5, querying the dependency graph rather than the component in isolation, that surfaces the single point of failure: three T3 systems share one embedding pipeline, so a failure or a poisoning of that pipeline is a T3-consequence event, whatever its own scorecard says.

## What these examples show together

- The scheme is proportionate at the low end (example 1) and non-compensatory at exactly the points where compensation would be a category error (examples 2, 3, 4) — it does not over-govern the summariser to prove it can over-govern something.
- **Example 2 is invisible to both external regimes it might plausibly fall under** — the revised MRM guidance excludes it by its narrowed model definition, and it contains no AI for an AI-specific regime to catch. The floors are the only reason it is tiered T3 instead of quietly running at whatever governance its owning team improvised.
- The agentic gap rule (F8, example 3) and the D9=4 anchor it depends on exist because "the model changed" no longer means "someone released new code" — it can mean a supplier updated a foundation model overnight, invisibly to any change-control process built around code releases.
- Mitigation credit is a live mechanism, not a one-off form: example 3's claimed control lapses automatically, without a review meeting or a missed calendar reminder being the trigger.
- Aggregate risk (example 4) is invisible to any tiering exercise that only ever looks at one system at a time — it requires querying the dependency graph, not just the component.
