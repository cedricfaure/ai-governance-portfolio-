> Component of the [Model Risk Tiering Scheme](../README.md) framework.

# The ten dimensions

Three families. Each dimension scores 1–5 with mandatory anchors.

## Family A — Impact (40%): what happens if it is wrong

### D1 · Consequence severity (within-family weight 40%)

1. Inconvenience only; no material loss
2. Minor financial, operational or reputational loss; readily absorbed
3. Material financial loss, service disruption, or a person's experience meaningfully degraded
4. Loss of access to a service, benefit, employment, credit or opportunity; significant financial detriment; discriminatory outcome
5. Risk to physical safety, health, liberty or fundamental rights; catastrophic financial or systemic loss

### D2 · Affected parties and vulnerability (30%)

1. A single internal user
2. Internal teams
3. External customers or citizens, in ordinary circumstances
4. Large affected populations, or individuals in circumstances of dependence or constrained choice
5. Children, patients, detainees, benefit claimants, or others in a legally recognised vulnerable position; or population-scale effect

### D3 · Reversibility and contestability (30%)

1. Trivially reversible; no persistent record
2. Reversible within the normal working cycle
3. Reversible with deliberate effort; a correction record persists
4. Difficult to reverse; harm accrues before correction; contestability exists but is burdensome
5. Irreversible, or no practical route to challenge the outcome

## Family B — Agency (35%): how much it decides, and how much rides on it

### D4 · Autonomy and action scope (40%)

This is the dimension the revised MRM guidance leaves unaddressed and the reason the framework exists in its current form. Score on what the system can do, not on what it is built from.

1. Produces information only; a human reads it and decides independently
2. Produces a recommendation; a human approves each instance before any action
3. Acts autonomously within a pre-approved, enumerated action set; escalates anything outside it
4. Acts autonomously within a broad operational boundary; continuous monitoring; hard constraints on resources, scope and time horizon
5. Initiates irreversible or externally visible actions without per-instance human confirmation; or invokes tools, spawns sub-tasks, or delegates to other systems

### D5 · Decision weight and human reliance (30%)

Measures automation bias exposure — how likely the nominal human reviewer is to defer.

1. One input among many; the human has independent grounds to decide
2. Influential input; independent verification is routine and practical
3. Primary input; verification is possible but seldom performed
4. Determinative in practice; override is technically available but rare, or discouraged by throughput expectations
5. Effectively determinative; no realistic verification route, or override carries a personal cost to the reviewer

**Note.** A system scoring 2 on autonomy and 5 on decision weight is not meaningfully supervised. Rubber-stamped human-in-the-loop is the most common false control in AI governance, and separating these two dimensions is what makes it visible. A large gap between D4 and D5 should be read as a finding.

### D6 · Exposure and materiality (30%)

Follows the revised MRM guidance's construction: purpose together with exposure determines materiality, where exposure is the significance of the output to business decisions (quantitatively measurable, e.g. by portfolio size) and purpose is qualitative — with systems supporting regulatory requirements generally considered higher risk.

1. Negligible volume or value; no regulatory purpose
2. Modest volume or value; internal purpose
3. Significant volume or value; business-critical purpose
4. Large portfolio or transaction value; or supports a regulatory obligation, statutory duty, or external reporting
5. Enterprise-material exposure; or directly determines regulatory, capital, prudential or statutory outcomes

## Family C — Uncertainty (25%): how confident we can be

### D7 · Opacity (25%)

1. Fully transparent, deterministic, inspectable logic
2. Interpretable model; behaviour explainable per instance
3. Complex model; global explanation available, per-instance explanation approximate
4. Opaque; explanations are post-hoc reconstructions rather than accounts of the actual computation
5. Opaque and non-deterministic; identical inputs may yield different outputs; no reliable per-instance explanation

### D8 · Data sensitivity and provenance (25%)

1. Public or synthetic data; provenance fully documented
2. Internal non-personal data; provenance documented
3. Personal data; lawful basis established; provenance largely documented
4. Special-category, financial, health, biometric or children's data; or partially undocumented provenance
5. Special-category data with unclear lawful basis, undocumented provenance, scraped sources, or unresolved rights over training data

### D9 · Behavioural volatility (25%)

1. Static; changes only by controlled release
2. Periodic retraining under change control
3. Frequent retraining, or sensitive to input distribution shift
4. Behaviour changes without a code release — prompt, configuration, retrieved context, or a supplier-side model update
5. Continuously learning or self-modifying in production; or behaviour materially dependent on a third-party model that may change without notice

**Note on D9 level 4.** This is the characteristic that most decisively breaks inherited MRM assumptions. A change-control regime keyed to code releases does not see a system whose behaviour changed because a supplier updated a model or someone edited a prompt. Any system scoring 4 or 5 here needs behavioural monitoring, not release monitoring.

### D10 · Third-party dependency (25%)

1. Fully in-house; no external runtime dependency
2. External components, fully documented, contractually controlled
3. Vendor system with adequate documentation and contractual assurance rights
4. Vendor or foundation model with limited visibility into training data, evaluation or update policy
5. Critical dependency on an opaque third party with no assurance rights, no notice of change, and no substitution path

**On proprietary opacity.** Limited visibility into a vendor component is a legitimate commercial reality and scores here honestly. It is not a reason to exempt the system — the organisation deploying it remains accountable for its use.
