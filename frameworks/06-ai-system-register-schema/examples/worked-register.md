> Component of the [AI System Register Schema](../README.md) framework.

# Worked register

**All entries are illustrative constructions. They describe no real organisation, engagement or system.**

`sample-register.csv` contains fifteen entries: the twelve systems from the worked classification examples, plus three seeded to exercise the validator, one orphan (AIR-0013, no business_owner), one broken dependency (AIR-0014, depends on a system_id that does not exist), and one internally contradictory entry (AIR-0015, `in_the_loop` oversight recorded against a `makes` decision role).

## The register as built

Twelve base entries carry the classification examples through as full register entries, populated to Layer 2 where their risk tier reaches T2 or above. Discovery sources are deliberately mixed rather than uniform, five arrived through `intake_process`, three through `declared_by_team`, and the rest are split across `saas_admin_sweep`, `endpoint_browser`, `identity_oauth`, `local_agentic_sweep`, `amnesty` and `network_log`, a realistic-looking spread rather than a register where everything was self-reported.

Four entries (AIR-0002, AIR-0005, AIR-0008, AIR-0012) declare `AIR-0011`, the shared document embedding pipeline, as a dependency.

## Validator output

```
$ python3 tool/register.py validate examples/sample-register.csv --schema schema

Entries: 15

ERRORS (4):
  [SCHEMA] AIR-0013: missing required field 'business_owner' (Layer 1)
  [R1] AIR-0015: human_oversight_model: in_the_loop with decision_role: makes is internally contradictory (section 1.9)
  [R4] AIR-0013: No business_owner, orphan
  [R7] AIR-0014: depends_on references a system_id not in the register, broken dependency (references 'AIR-9999')

WARNINGS (10):
  [R2] AIR-0005: decision_role: supports_genuine with no override-rate evidence field populated, see section 1.7 evidence test
  [R3] AIR-0002: affects_people: external_individuals and decision_role in (makes, supports_determinative) and no Layer 3 populated, probable registration trigger
  [R3] AIR-0003: affects_people: external_individuals and decision_role in (makes, supports_determinative) and no Layer 3 populated, probable registration trigger
  [R3] AIR-0006: affects_people: external_individuals and decision_role in (makes, supports_determinative) and no Layer 3 populated, probable registration trigger
  [R3] AIR-0015: affects_people: external_individuals and decision_role in (makes, supports_determinative) and no Layer 3 populated, probable registration trigger
  [R5] AIR-0001: lifecycle_status: in_use and next_review_due in the past, stale
  [R5] AIR-0008: lifecycle_status: in_use and next_review_due in the past, stale
  [R8] AIR-0001: provenance: embedded_feature and vendor does not name a parent product
  [R9] AIR-0009: system_type in agentic category and no systems_integrated recorded, action scope unknown
  [R10] AIR-0010: lifecycle_status: in_trial and no risk_tier, pilots are not exempt, section 1.8

Exit code: 1
```

**Reading the errors.** AIR-0013 produces two findings for the same underlying problem, a `[SCHEMA]` error (business_owner is a required Layer 1 field) and an `[R4]` error (the named orphan rule). That duplication is deliberate, not a bug, see `tool/README.md` for why: the schema check confirms the record is structurally incomplete, and R4 gives the specific governance failure a name and a citation. AIR-0015 is the internal-contradiction case: recording `in_the_loop` oversight against a `makes` decision role claims both that a human approves every output before it takes effect, and that no person reviews it. Only one can be true. AIR-0014's broken dependency is exactly the kind of error that a spreadsheet with no validation would carry silently for years.

**Reading the warnings.** AIR-0005 is the `supports_genuine` claims that must be evidenced, not assumed, playbook step 15 in practice: nothing in `monitoring_in_place` supports the claim that adjusters genuinely override the claims triage scorer, so the warning fires and the entry should be re-examined before its classification is trusted. AIR-0009, the MCP server on a developer laptop, has no recorded `systems_integrated`, which is the point, it is exactly the kind of exposure that is easy to switch on and hard to scope after the fact. AIR-0010 is `in_trial` with no risk tier, the "register, then decide" case from the classification examples, caught here as a live warning rather than an assumption that pilots are exempt.

## Health metrics

```
$ python3 tool/register.py health examples/sample-register.csv --schema schema

Total entries: 15

  Coverage confidence          N/A                target: >60%         N/A, not captured by a single discovery_source field

  Discovery mix (share of entries by discovery_source):
    intake_process          5  (33%)
    declared_by_team        3  (20%)
    saas_admin_sweep        2  (13%)
    endpoint_browser        1  (7%)
    identity_oauth          1  (7%)
    local_agentic_sweep     1  (7%)
    amnesty                 1  (7%)
    network_log             1  (7%)
  Discovery mix headline: intake_process = 33% (target: majority at maturity) [ATTENTION]

  Orphan rate                  7%                 target: 0%           ATTENTION
  Staleness                    17%                target: <10%         ATTENTION
  Attestation rate             N/A                target: >90%         N/A, no attestation field in this schema
  Tier coverage (proxy)        87%                target: 100%         ATTENTION
  Undeclared discovery rate (proxy) 40%               target: declining, never zero  TREND METRIC, needs history
  Disclosure gap               10                 target: 0            ATTENTION
```

**Reading this.** A fifteen-entry register with a single orphan, two stale reviews, and ten entries affecting people with no recorded transparency disclosure is not a healthy register, and the metrics say so honestly rather than averaging the problems away. The 33% intake_process share is below the "majority at maturity" target, appropriately: this register was just built through a discovery exercise, not run day to day for a year. Two metrics, coverage confidence and attestation rate, are reported as not computable rather than guessed at, see `tool/README.md` for exactly why.

## Dependency graph

```
$ python3 tool/register.py graph examples/sample-register.csv --schema schema

Dependency edges (system depends_on upstream):
  AIR-0002 -> AIR-0011
  AIR-0005 -> AIR-0011
  AIR-0008 -> AIR-0011
  AIR-0012 -> AIR-0011
  AIR-0014 -> AIR-9999  [UNRESOLVED]

Cycles:
  none

Shared components (2 or more dependants):
  AIR-0011: 4 dependants (AIR-0002, AIR-0005, AIR-0008, AIR-0012)
    component risk_tier: (not tiered)
    highest dependant risk_tier: T3
    FLAG: tier inversion, dependants reach T3 while the shared component is untiered. Framework 03 section 1.11 rule 5: tier at the maximum of dependants.
```

AIR-0011, the shared document embedding pipeline, has never been tiered on its own account, there is no obvious reason to: on its own it makes no decision and touches no one directly. But four systems depend on it, one of which (AIR-0008, the procurement agent) reaches T3. Standalone tiering would leave this component invisible in every dashboard that sorts by risk tier. The graph command is what surfaces it, exactly the pattern Framework 03 section 1.11 rule 5 describes, and exactly why the register carries a `depends_on` field at all rather than treating every entry as independent.

## What a system count would not reveal

Fifteen entries and a count of "how many AI systems do we have" tells a board almost nothing. What the validator, the health metrics and the graph reveal together is different: which entries are ungoverned (the orphan), which claims of human oversight do not hold up against the entry's own other fields (the contradiction), which systems affecting real people have no public disclosure to match (ten of them), and which single component sixteen percent of the register's build effort would break if it failed silently (the embedding pipeline). None of that is visible from a number. It is only visible from a register that is queried, not just counted.

### What this example is designed to show

- Entries 3 and 6 (the grant scoring spreadsheet and the benefit eligibility rules engine) contain no AI at all and are among the highest-consequence entries in the register, exactly the systems a technology-anchored inventory would miss entirely.
- Entry 2's `supports_determinative` classification is the uncomfortable one: a human reviews every ranked shortlist, but the notes record that recruiters rarely go below the ranked fold, which is precisely the rubber-stamp pattern the schema is built to catch rather than paper over.
- A validation error can legitimately come from two different layers at once (AIR-0013's SCHEMA and R4 findings), and that is a feature of keeping structural completeness and named governance rules separate, not a defect to be deduplicated away.
- Two of the eight health metrics cannot be computed from this schema alone, and the tool says so rather than manufacturing a reassuring number, the same discipline the wider portfolio applies to compliance-cost figures elsewhere.
- A component that makes no decision and touches no personal data (the shared embedding pipeline) can still be the single most consequential entry in the register, once its dependants are taken into account, and only a dependency graph, not a spreadsheet sorted by risk tier, will show that.
