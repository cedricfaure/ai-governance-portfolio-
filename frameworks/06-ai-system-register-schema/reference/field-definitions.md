> Component of the [AI System Register Schema](../README.md) framework.

# The three-layer schema, field definitions

The single biggest reason registers fail is that the field set is too heavy for the low-risk majority. This schema solves that with progressive disclosure: everything gets Core; only what matters gets more.

Rule: Layer 1 is mandatory for every system, without exception, and must be completable in under ten minutes by someone who is not a governance specialist. If it takes longer, the register will not be populated and everything downstream fails.

## Layer 1, Core (14 fields, every system)

| # | Field | Type | Definition | Example |
|---|---|---|---|---|
| 1 | system_id | string | Unique persistent identifier. Never reused. | AIR-0042 |
| 2 | name | string | What it is called internally | Claims triage scorer |
| 3 | description | text | One plain sentence on what it does | Scores inbound claims for fast-track eligibility |
| 4 | purpose | text | The decision or task it exists to perform | Route claims to fast-track or manual review |
| 5 | business_owner | person | Named individual accountable inside the organisation. Never a vendor, never a team. | A. Rahman, Head of Claims |
| 6 | technical_owner | person | Named individual accountable for it working | S. Okafor, Data Engineering |
| 7 | system_type | enum | See taxonomies.md | predictive_model |
| 8 | provenance | enum | See taxonomies.md | embedded_feature |
| 9 | decision_role | enum | See taxonomies.md, the highest-value field in the register | supports |
| 10 | affects_people | enum | no / internal_staff / external_individuals | external_individuals |
| 11 | data_categories | multi | Plain-language categories consumed | claim history; personal identifiers |
| 12 | lifecycle_status | enum | See taxonomies.md | in_use |
| 13 | discovery_source | enum | How this entry was found. See taxonomies.md | declared_by_team |
| 14 | date_registered | date | First entry date | 2026-09-09 |

## Layer 2, Extended (16 further fields, T2 and above)

| # | Field | Type | Definition |
|---|---|---|---|
| 15 | risk_tier | enum | T0 to T4 from Framework 03 |
| 16 | tier_date | date | When the tier was assigned |
| 17 | tier_ruleset_version | string | Which rule-set version produced it |
| 18 | process_owner | person | Accountable for the business process it sits in |
| 19 | vendor | string | Supplier, or in-house. For embedded features, name the parent product too. |
| 20 | underlying_model | string | Model or family where known, including version |
| 21 | model_provenance | enum | in_house / open_weights / commercial_api / embedded_unknown |
| 22 | human_oversight_model | enum | See taxonomies.md |
| 23 | autonomy_level | int 1 to 5 | Framework 03 dimension D4 |
| 24 | decision_weight | int 1 to 5 | Framework 03 dimension D5 |
| 25 | volume | string | Decisions or actions per period |
| 26 | systems_integrated | multi | Systems it reads from or writes to |
| 27 | depends_on | multi | system_id list, upstream dependencies |
| 28 | data_residency | string | Where data is processed and stored |
| 29 | monitoring_in_place | enum | none / availability / performance / drift_and_subgroup / continuous_behavioural |
| 30 | last_reviewed / next_review_due | date | Per tier cadence |

## Layer 3, Regulatory (14 further fields, where a trigger fires)

| # | Field | Definition |
|---|---|---|
| 31 | regimes_in_scope | Applicable regimes, per jurisdiction, populated locally |
| 32 | classification_per_regime | Classification under each |
| 33 | organisational_role | Role under each regime where the regime distinguishes roles |
| 34 | registration_required | Whether external registration is required |
| 35 | registration_reference | External registration or database reference number |
| 36 | registration_date | Date registered externally |
| 37 | lawful_basis | Lawful basis for processing personal data |
| 38 | impact_assessment_ref | Reference to the completed assessment |
| 39 | impact_assessment_date | Date completed |
| 40 | transparency_disclosure | Where the use is disclosed to affected people |
| 41 | contestability_route | How a person challenges an outcome |
| 42 | retention_and_logging | Log retention arrangement |
| 43 | conformity_evidence_ref | Reference to the conformity or assurance file |
| 44 | substantial_modification_log | Changes triggering re-registration |

## On Layer 3

Registration obligations exist in several regimes. As one concrete example, under the EU AI Act, Article 49 requires providers, and in defined cases deployers, including public authority deployers, to register Annex III high-risk systems in the EU database established under Article 71 before placing on the market or putting into service, using the structured information set out in Annex VIII, and to update entries following a substantial modification. Certain information is publicly accessible. Registration is a pre-launch step, not a post-launch formality.

Other jurisdictions impose different triggers. As a second example, Australian Privacy Principles 1.7 to 1.9 require organisations to set out in their privacy policy the automated decisions that significantly affect people, from 10 December 2026, a disclosure obligation which cannot be drafted without a register that records the decision role of each system.

Do not pre-populate the regime mappings in this repository. The framework supplies the field structure; authoritative mappings require primary-source work per jurisdiction.
