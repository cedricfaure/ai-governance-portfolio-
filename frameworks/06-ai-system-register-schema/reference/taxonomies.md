> Component of the [AI System Register Schema](../README.md) framework.

# Taxonomies

## System type

Traditional inventories were built for applications. AI estates contain three fundamentally different things, and the governance question differs for each.

| Category | Type value | Definition | Examples |
|---|---|---|---|
| Application | genai_assistant | Conversational or generative tool used by staff | Chat assistant, drafting tool |
| | embedded_saas_ai | AI feature inside a product bought for another purpose | CRM lead scoring, HR CV ranking |
| | predictive_model | Statistical or ML model producing a score, class or forecast | Churn model, claims triage, credit scorecard |
| | rules_engine | Deterministic logic driving a consequential decision | Eligibility matrix, pricing rules |
| | spreadsheet_model | Scoring or eligibility model in a spreadsheet | Grant scoring workbook |
| | browser_extension | AI running inside the browser session | Summariser, meeting notetaker |
| | coding_assistant | AI generating or reviewing code | Code completion, PR review bot |
| Infrastructure | model_api | Externally hosted model accessed by API | Foundation model endpoint |
| | local_model_runtime | Model running on local or self-hosted infrastructure | On-prem inference server, laptop runtime |
| | vector_store_rag | Retrieval infrastructure serving model context | Embedding store, RAG pipeline |
| | ml_platform | Training, serving or feature infrastructure | Feature store, model registry |
| Agentic | agent | System that plans and acts, invoking tools | Procurement agent, triage agent |
| | agent_framework | Orchestration layer for agents | Orchestrator, planner |
| | mcp_client | Component consuming tool servers | IDE agent with tool access |
| | mcp_server | Component exposing tools, data or actions to a model | Local server exposing a database |

**Why the agentic category is separate.** An assistant that drafts text and an agent that can write to a production database are not variants of the same thing, they are different governance problems. The inventory must capture what a system can do, not what it is built from. Local agentic components in particular, MCP servers on developer machines, local runtimes, agent frameworks, are the fastest-growing blind spot, and they appear in no traditional SaaS inventory.

## Provenance

Determines who you can ask questions of, and what assurance is available.

| Value | Definition | Governance implication |
|---|---|---|
| built_in_house | Developed internally | Full visibility; full accountability |
| bought_standalone | Procured as an AI product | Contractual assurance rights should exist, check they do |
| embedded_feature | AI inside a product bought for something else | Never separately procured, so never reviewed. Highest miss rate. |
| accessed_free_tier | Consumer or free-tier tool used for work | No contract, no data guarantees, often no visibility |
| open_weights_self_hosted | Open model run on own infrastructure | Full control; full responsibility for evaluation |
| agent_or_extension | Installed by an individual user | Often unmanaged; often privileged |

`embedded_feature` is the field that finds the most systems. The feature was switched on without a separate purchase, so it never reached a procurement gate, never got a security review, and never reached any register. Treat every embedded AI feature as in scope until ruled out.

## Decision role

The single highest-value field in the register. It determines regulatory exposure, drives Framework 03's D4 and D5 dimensions, and is the field most disclosure obligations turn on. It is also the one most often recorded optimistically.

| Value | Definition | Test |
|---|---|---|
| makes | The system decides. No person reviews before the outcome takes effect. | Does the outcome reach the person without a human seeing it? |
| supports_determinative | A person nominally reviews, but in practice defers | Is override technically available but rare, under throughput pressure, or without independent grounds to disagree? |
| supports_genuine | A person genuinely reviews and can overturn, with capacity and authority | Does the reviewer have time, information and standing to disagree, and do they measurably do so? |
| informs | One input among several; the person decides independently | Would the decision be made anyway, differently sourced? |
| no_decision | Produces no decision or action consequence | (none) |

The `supports_determinative` category is deliberate and is the most important design choice in the schema. Most registers offer only "makes" or "supports", and almost everything gets recorded as "supports" because a human is nominally in the loop. That collapses the distinction between real oversight and a rubber stamp, and rubber-stamped human-in-the-loop is the most common false control in AI governance.

**The evidence test.** If you cannot state the override rate for a system recorded as `supports_genuine`, you do not know that it is. An override rate near zero means the classification is `supports_determinative`, whatever the process document says. Measure it before claiming it.

## Lifecycle status

| Value | Definition | Register implication |
|---|---|---|
| proposed | Under consideration; not built | On the register from intake |
| in_development | Being built | Tier before build approval |
| in_trial | Pilot with real data or real users | Full obligations apply. A pilot touching real people is not exempt. |
| in_use | Live in production | Full obligations |
| suspended | Temporarily stopped | Retained; reason recorded |
| being_retired | Decommissioning in progress | Dependency check required before removal |
| retired | No longer in use | Retained, not deleted |
| out_of_scope | Assessed and excluded | Retained with reasoning |

Two rules: a register showing only live systems misses the one going to production next month; and retired entries are never deleted, because "what were we using in March" is a question that gets asked after an incident.

## Human oversight model

| Value | Definition |
|---|---|
| none | No human involvement in the loop |
| on_the_loop | Human monitors and can intervene, but does not approve individually |
| sampled_review | A defined sample is reviewed after the fact |
| in_the_loop | Human approves each consequential output before effect |
| human_decides | System advises only; the human makes the decision |

**Consistency rule.** This field must be coherent with `decision_role` and `autonomy_level`. A system recorded as `in_the_loop` oversight and `makes` decision role is internally contradictory, one of the two is wrong. The validator must flag this pairing.

## Discovery source

Record how each entry was found: `declared_by_team`, `amnesty`, `network_log`, `identity_oauth`, `endpoint_browser`, `saas_admin_sweep`, `expense_procurement`, `local_agentic_sweep`, `incident`, `audit`, `intake_process`.

This field is the register's own quality metric. If 95% of entries are `declared_by_team`, discovery has not run. A healthy mature register shows most new entries arriving through `intake_process`, because the front door is working, and continues to show a trickle from technical layers, because it always will.
