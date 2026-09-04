> Component of the [Model Risk Tiering Scheme](../README.md) framework.

# Why this framework exists now — the SR 26-2 gap

For fifteen years, the reference discipline for tiering model risk was the 2011 interagency supervisory guidance on model risk management — Federal Reserve SR 11-7 and OCC Bulletin 2011-12, adopted by the FDIC in 2017. Its core apparatus — a firm-wide model inventory, risk-based tiering by materiality, independent validation through effective challenge, ongoing monitoring — became the template far beyond banking.

On 17 April 2026, that guidance was superseded. The Federal Reserve, OCC and FDIC jointly issued revised guidance (SR 26-2 / OCC Bulletin 2026-13), which:

- Narrows the definition of "model" to a complex quantitative method, system or approach applying statistical, economic or financial theories to process input into quantitative estimates — explicitly excluding simple arithmetic calculations such as those found in spreadsheets, and deterministic rule-based processes and software with no statistical, economic or financial theory underpinning their design or use.
- Explicitly excludes generative and agentic AI models from scope, on the basis that these technologies are novel and rapidly evolving — while confirming that the guidance does apply to traditional statistical and quantitative models and to non-generative, non-agentic AI models.
- Introduces a $30 billion total asset applicability threshold, while noting it may still be relevant to smaller institutions with significant model risk exposure.
- Establishes that model purpose together with model exposure determines model materiality, where exposure refers to the significance of the model output to business decisions and can be quantitatively measured, and purpose is a qualitative consideration — with models developed to help meet regulatory requirements generally considered higher risk.
- Removes the prescribed annual validation cadence in favour of materiality-driven review.
- States explicitly that it does not set forth enforceable standards or prescriptive requirements, and that non-compliance will not itself result in supervisory criticism.

The agencies have signalled a forthcoming request for information addressing model risk management and, in particular, banks' use of AI including generative and agentic AI.

**Why this matters far beyond banking.** The revised guidance is careful on this point: systems outside its scope are not outside governance. It directs organisations to apply their broader risk management and governance practices to determine appropriate controls for anything not covered — including generative and agentic AI.

The practical consequence is a structural gap, and it is the gap this framework fills:

| Asset class | Covered by revised MRM guidance? | Covered by product/AI regulation? |
|---|---|---|
| Traditional statistical models | Yes | Sometimes, by application context |
| Non-generative, non-agentic AI | Yes | Sometimes, by application context |
| Generative AI | No — explicitly excluded | Sometimes, by application context |
| Agentic AI | No — explicitly excluded | Emerging and incomplete |
| Deterministic rule engines and spreadsheets driving consequential decisions | No — excluded by the narrowed definition | Generally not |

Three observations follow, and they justify the design in the ten-dimensions section of this framework:

1. **The fastest-moving, least-understood systems now sit outside the most mature tiering discipline.** An organisation relying solely on an MRM inventory has a growing blind spot precisely where novelty is highest.
2. **Regulatory regimes tier by application context, not by technology.** A system's risk classification under a product-safety-style AI regime depends on what decision it touches, not what it is built from. An internal scheme must therefore be technology-agnostic and application-anchored, or it will not cross-walk.
3. **Narrowing the definition of "model" removes governance from tools that still drive consequential outcomes.** A deterministic rules engine that denies benefit applications is out of MRM scope and always was out of AI-specific scope — yet it is exactly the kind of system that generates administrative-law problems.

**The framework's position:** an internal tiering scheme must be broader than any single external regime, anchored on consequence rather than technology, and explicitly capable of tiering systems that no external regime currently claims. External classifications are then treated as floors the internal scheme must respect, not as the scheme itself.

## Scope — what gets tiered

Tier any system that influences a decision or takes an action with a consequence, irrespective of its technical construction. Specifically in scope:

- Statistical and machine learning models
- Generative AI systems, including those built on third-party foundation models
- Agentic systems that plan, invoke tools, or act
- Deterministic rule engines and scoring matrices driving consequential decisions
- Vendor and embedded AI features within procured software
- Material end-user computing artefacts where the output drives a consequential decision
- Composite systems and chains where the output of one feeds another

Explicitly out of scope: systems with no decision or action consequence — pure visualisation, unaggregated reporting, and internal experimentation in an isolated environment with no production data and no production output.

**The definitional rule: scope is determined by consequence, not by construction.** A spreadsheet that determines eligibility is in scope. A neural network that recommends canteen menus is, at most, Tier 1. Anchoring scope on technology is the error that produced the current gap; do not repeat it internally.

**On vendor systems:** procurement does not transfer accountability. A vendor system is tiered on the consequence of its use in your organisation, not on the vendor's own classification. Limited visibility into a proprietary component is a scoring input on the opacity dimension, not an exemption.
