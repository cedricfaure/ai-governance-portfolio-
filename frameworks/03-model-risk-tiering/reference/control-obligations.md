> Component of the [Model Risk Tiering Scheme](../README.md) framework.

# Control obligations by tier, and residual tier / mitigation credit

## Control obligations by tier

This is the operative table — the point at which tiering becomes governance rather than labelling. Every cell is a binding obligation.

| Control domain | T1 Limited | T2 Moderate | T3 High | T4 Critical |
|---|---|---|---|---|
| Registration | Inventory entry | Inventory + business card | Full record + cross-walk | Full record + board-visible register |
| Approval authority | Process owner | Function head | Risk committee | Executive committee, with risk sign-off |
| Pre-deployment validation | Self-assessment | Documented internal review | Independent review by a party outside the build team | Independent review + external assurance or peer review |
| Effective challenge | Not required | Peer review | Independent, documented, with recorded resolution | Independent, documented, plus adversarial review |
| Testing | Functional | Functional + baseline performance | Performance, robustness, bias evaluation across relevant subgroups | All, plus adversarial and scenario testing across full decision paths |
| Human oversight | None required | Human decides; system advises | Human review with genuine capacity and authority to override | Human confirmation before consequential action; documented override rights and protections |
| Documentation | Purpose, owner, inputs | + method, data sources, limitations | + full technical file, assumptions, known failure modes, evaluation results | + decision rationale, residual risk acceptance, minuted approval |
| Monitoring | Availability | + performance against baseline | + drift, subgroup performance, override and exception rates | + continuous behavioural monitoring, real-time anomaly alerting |
| Monitoring cadence | Annual | Quarterly | Monthly | Continuous, with defined response times |
| Logging | Standard application logs | Decision logs | Decision logs with inputs and rationale, retained per policy | Full trajectory logs including tool calls and intermediate reasoning steps |
| Revalidation | On material change | Every 24 months or on trigger | Every 12 months or on trigger | Every 6 months or on trigger |
| Incident response | Standard IT process | Defined process with named owner | Defined playbook, escalation path, notification assessment | Playbook + rehearsed response + standing kill switch tested at defined intervals |
| Impact assessment | Not required | Screening | Full assessment | Full assessment + external or independent input |
| Contestability | Not applicable | Feedback route | Documented challenge route with defined response time | Formal appeal to a human with authority to reverse |
| Third-party assurance | Not required | Vendor attestation | Contractual assurance rights + evidence review | Right to audit + change notification + tested substitution plan |
| Decommissioning | Remove from inventory | Documented retirement | Retirement plan, data disposition, downstream dependency check | Full plan + transition arrangements + notification of affected parties |

**On monitoring cadence.** The revised MRM guidance removed the prescribed annual validation cadence in favour of materiality-driven review. This framework retains explicit cadences by tier for a practical reason: "risk-based frequency" without a stated default becomes "when someone remembers." The cadences above are the default; deviation is permitted where justified, documented and approved at the tier's approval authority.

## Residual tier and mitigation credit

The Inherent Tier is the tier of record. The Residual Tier exists to allow proportionate assurance effort where controls are genuinely in place and demonstrated.

Mitigation credit is earned, not claimed. Adopting the discipline used in Canada's AIA — where credit is given only for mitigation measures that are documented and in place, not planned or aspirational — this framework requires, for each claimed control:

- A named owner
- Documented evidence of operation, not of design
- A test or assurance result dated within the tier's monitoring cadence
- An identified failure mode it addresses, traceable to a specific dimension

**Rules:**

- Maximum reduction is one tier. Never more, at any evidence level.
- Never below any triggered floor.
- Never from T4. Critical systems do not become high-risk systems because they are well managed; that is what "critical" means.
- Never below T1.
- Residual tier modulates validation depth, monitoring cadence and reporting frequency only.
- Residual tier does not alter: regulatory obligations, human oversight requirements, approval authority, or incident escalation path. These follow the Inherent Tier.
- Residual credit lapses automatically if evidence is not refreshed within the cadence. Lapse returns the system to its Inherent Tier without a decision, review or grace period. This must be automatic in the tooling, because a lapse that requires someone to notice it will not happen.
