> Component of the [AI System Register Schema](../README.md) framework.

# Worked classification examples

All examples below are illustrative constructions and describe no real system.

The taxonomies above are only useful if the edge cases are settled. These are the calls that come up in practice.

| # | System | system_type | provenance | decision_role | affects_people | Notes |
|---|---|---|---|---|---|---|
| 1 | CRM lead scoring switched on by Sales | embedded_saas_ai | embedded_feature | informs | external_individuals | Classic miss. In scope. Low tier, but registered. |
| 2 | HR platform ranking job applicants | embedded_saas_ai | embedded_feature | supports_determinative | external_individuals | Recruiters rarely go below the ranked fold. Override rate will confirm. |
| 3 | Spreadsheet scoring grant applications | spreadsheet_model | built_in_house | makes | external_individuals | Not "AI", not software, fully in scope. |
| 4 | Meeting notetaker extension | browser_extension | agent_or_extension | no_decision | internal_staff | No decision, but records confidential discussion. Registered for data reasons. |
| 5 | Claims triage model routing to fast-track | predictive_model | built_in_house | supports_genuine | external_individuals | Only if adjusters demonstrably override. Otherwise reclassify. |
| 6 | Eligibility rules engine for a benefit | rules_engine | built_in_house | makes | external_individuals | Deterministic, transparent, and among the highest-consequence entries. |
| 7 | Code completion in developer IDEs | coding_assistant | bought_standalone | informs | no | Low governance weight; matters for IP and code provenance. |
| 8 | Procurement agent issuing POs under a threshold | agent | built_in_house | makes | no | Acts autonomously. High autonomy despite no personal data. |
| 9 | MCP server on a developer laptop exposing a database | mcp_server | agent_or_extension | no_decision | no | No decision, significant exposure. Register it. |
| 10 | Free-tier chatbot used by marketing | genai_assistant | accessed_free_tier | informs | no | No contract. Data handling unknown. Register, then decide. |
| 11 | Shared embedding pipeline serving four systems | vector_store_rag | built_in_house | no_decision | no | Trivial standalone; critical as a dependency. |
| 12 | Chatbot answering customer policy questions | genai_assistant | bought_standalone | informs | external_individuals | Reclassify to makes the moment it starts confirming entitlements. |

## What these examples are designed to settle

- Entries 1, 2 and 12 are embedded or bought features nobody procured as "AI"
- Entries 3 and 6 contain no AI at all and are among the most consequential
- Entries 4, 9 and 11 make no decisions and still belong on the register, for data exposure and dependency reasons
- Entry 5 is the supports_genuine claim that must be evidenced, not assumed
- Entry 8 shows autonomy is a separate axis from personal data
