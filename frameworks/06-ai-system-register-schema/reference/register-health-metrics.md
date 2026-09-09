> Component of the [AI System Register Schema](../README.md) framework.

# Register health metrics

Report these, not the raw count. The count only tells you how hard you looked.

| Metric | Definition | Target | Reads as |
|---|---|---|---|
| Coverage confidence | Share of entries corroborated by 2 or more independent discovery sources | >60% | Do we believe the register? |
| Discovery mix | Share of new entries by discovery_source | Majority intake_process at maturity | Is the front door working? |
| Orphan rate | Entries with no named business owner | 0% | Nothing is ungoverned |
| Staleness | Share past next_review_due | <10% | Is it current? |
| Attestation rate | Owners confirming entries within cadence | >90% | Do owners engage? |
| Tier coverage | T2+ entries with a current tier | 100% | Is triage complete? |
| Undeclared discovery rate | New systems found by technical layers per quarter, post-amnesty | Declining, never zero | Is intake capturing new adoption? |
| Disclosure gap | Systems affecting people not covered by a public disclosure | 0 | The board-level number |

Undeclared discovery rate should never reach zero. A zero means discovery stopped running, not that shadow AI ended. Treat a sudden drop as a tooling failure until proven otherwise.
