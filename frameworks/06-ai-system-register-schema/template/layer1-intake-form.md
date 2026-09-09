<!--
AI System Register, Layer 1 intake form.
Completable in under ten minutes by someone who is not a governance
specialist. See ../README.md for the framework this form belongs to.
-->

# Layer 1 intake form

Fourteen questions. If you are unsure of an answer, write your best guess and flag it, do not leave it blank and do not wait until you are certain.

**1. What do you want to call this, internally?**
*Example: "Claims triage scorer"*

**2. In one plain sentence, what does it do?**
*Example: "Scores inbound claims for fast-track eligibility."*

**3. What decision or task does it exist to help with?**
*Example: "Route claims to fast-track or manual review."*

**4. Who is accountable if this goes wrong?**
Name a person, not a team and not a vendor.
*Example: "A. Rahman, Head of Claims"*

**5. Who is accountable for it working technically?**
Name a person.
*Example: "S. Okafor, Data Engineering"*

**6. What kind of thing is it?** Pick the closest fit:
- A conversational or generative tool used by staff (`genai_assistant`)
- An AI feature inside a product bought for something else, e.g. your CRM or HR system (`embedded_saas_ai`)
- A model that produces a score, class or forecast (`predictive_model`)
- A fixed set of rules driving a decision, even if there is no AI involved (`rules_engine`)
- A scoring or eligibility spreadsheet (`spreadsheet_model`)
- Something running inside a browser (`browser_extension`)
- Something that writes or reviews code (`coding_assistant`)
- An externally hosted model reached by an API (`model_api`)
- A model running on a laptop or your own servers (`local_model_runtime`)
- Infrastructure that retrieves documents or context for a model (`vector_store_rag`)
- Platform infrastructure for training or serving models (`ml_platform`)
- Something that plans and takes action on its own (`agent`)
- Something that coordinates other agents (`agent_framework`)
- A component that consumes tools on behalf of a model (`mcp_client`)
- A component that exposes data, tools or actions to a model (`mcp_server`)

**7. Where did it come from?**
- Built by us (`built_in_house`)
- Bought as a standalone product (`bought_standalone`)
- A feature inside something bought for another purpose (`embedded_feature`)
- A free or personal-account tool people use for work (`accessed_free_tier`)
- An open model we run ourselves (`open_weights_self_hosted`)
- Installed by an individual, e.g. a browser add-on or an agent (`agent_or_extension`)

**8. Does its output reach a person without anyone reviewing it first?**
- Yes, nobody reviews it before it takes effect (`makes`)
- Someone reviews it, but in practice they rarely disagree (`supports_determinative`)
- Someone reviews it and genuinely can, and does, disagree (`supports_genuine`)
- It is one input someone considers alongside others (`informs`)
- It does not lead to any decision or action (`no_decision`)

If you are not sure whether reviewers genuinely disagree, say so. This is the single most important question on the form, and the honest answer is more useful than the comfortable one.

**9. Who is affected by what it produces?**
- Nobody outside the organisation (`no`)
- Colleagues (`internal_staff`)
- Customers, applicants, patients or members of the public (`external_individuals`)

**10. What kind of information does it use?**
Plain language, not technical categories.
*Example: "Claim history; names and addresses"*

**11. What state is it in right now?**
- Being considered (`proposed`)
- Being built (`in_development`)
- Being trialled with real data or real people (`in_trial`)
- Live (`in_use`)
- Paused (`suspended`)
- Being switched off (`being_retired`)
- Switched off (`retired`)
- Looked at and ruled out of scope (`out_of_scope`)

**12. How did you come to be telling us about this?**
*Example: "Someone asked me directly", "It came up in the team survey", "I raised it myself when starting the project"*

**13. Today's date.**

**14. Is there anything about this you think we should know that the questions above did not ask?**
