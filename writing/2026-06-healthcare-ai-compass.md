---
title: "The Healthcare AI Compass: Evidence, Adoption and What AI Professionals Get Wrong"
date: 2026-06-22
summary: >-
  A review of 200 healthcare AI use cases, shortlisted to 50 and mapped
  across seven clinical and operational categories against real-world
  evidence of impact and deployment maturity. The central finding is an
  inversion: the tools with the strongest clinical-outcome evidence are
  rarely the most widely deployed, while the tools deployed at greatest
  scale are frequently those for which clinical outcome evidence is
  weakest or contested — but backed by payers.
tags: [healthcare, evidence, adoption, regulatory, fda, clinical-ai]
status: published
---

# The Healthcare AI Compass: Evidence, Adoption and What AI Professionals Get Wrong

**Cédric M.G. Faure** — [LinkedIn](https://www.linkedin.com/in/cedric/)
Associate Director Data & AI @ Contango | AI Strategy, Data Governance, Public Sector, Energy
*June 22, 2026*

*Perspective • Health AI Literacy*

This article reviews 200, and shortlists 50, AI use cases to map them across
seven clinical and operational categories, and assesses them against
real-world evidence of impact and deployment maturity. The central finding
is an inversion: the tools with the strongest clinical-outcome evidence are
rarely the most widely deployed, while the tools deployed at greatest scale
are frequently those for which clinical outcome evidence is weakest or
contested, but backed by payers.

| Metric | Value |
| --- | --- |
| FDA AI devices authorised through Dec 2025 | **1,451** |
| LLM-based devices among those 1,451 | **0** |
| US hospitals using predictive AI in EHR, 2024 | **71%** |

## The adoption–evidence inversion

What I witness is that the commercial trajectory of healthcare AI does not
seem to follow its clinical evidence base. Ambient documentation scribes
reached $600 million in annual spend and deployment in over 60% of US Epic
hospitals before a single multi-centre randomised controlled trial measured
their impact on care delivery. Prior authorisation automation, for
instance, expanded to roughly three-quarters of health plans before
independent oversight bodies documented an 82% overturn rate on appealed
Medicare Advantage denials. In other words: wide adoption and investment
before disappointing results. On the opposite side of the spectrum,
mammography AI, supported by the largest randomised imaging trial in
history, enrolling 105,934 women across Swedish population-screening
programmes, has not achieved routine clinical adoption in any country.

This pattern repeats across the 50 use cases I've examined. Adoption
velocity correlates with administrative ROI and workflow acceleration, not
with the strength of evidence for patient benefit. The implication for
clinicians, health system leaders, and AI vendors is structural: the map
most Health-IT professionals follow does not reflect either the regulatory
record or the outcome evidence.

A second, compounding misalignment concerns the nature of AI itself. The
dominant public experience of it — AI as conversational chatbot, i.e. "just
ask Claude or ChatGPT" — describes a subset of the technology. The FDA has
yet to authorize a device that relies on generative AI. But a recent
breakthrough designation (note: this is not, *stricto sensu*, an
authorization) was granted to one: RecovryAI's LLM-powered post-surgical
recovery chatbot. As of today, I could not find a single FDA-cleared
LLM-based medical device, despite those models accounting for the majority
of industry attention and a large fraction of enterprise AI spend. The
overwhelming majority of clinical AI operating in hospitals today is
narrow, task-specific machine learning: convolutional networks reading
images, gradient-boosting models scoring sepsis risk, recurrent networks
predicting AKI onset. These tools are largely invisible to clinicians, and
their invisibility is itself a governance problem.

## The seven categories

The 50 use cases in this review organise into seven functional categories.
Each carries a distinct evidence profile, regulatory pathway,
reimbursement trajectory, and failure-mode pattern. The aggregation of all
seven under the label "healthcare AI" is the primary source of professional
misunderstanding in the field.

| Category | Use cases | Focus |
| --- | ---: | --- |
| **A** — Clinical Diagnostics & Imaging | 10 | Radiology, endoscopy, ECG interpretation |
| **B** — Clinical Decision Support & Risk Prediction | 9 | Sepsis, AKI, readmission, generative decision support |
| **C** — Administrative & Revenue Cycle | 5 | Ambient scribes, RCM, prior authorisation |
| **D** — Patient-Facing & Remote Care | 6 | Remote monitoring, wearables, mental-health chatbots |
| **E** — Drug Discovery & R&D | 5 | Protein structure prediction, trial matching, pharmacovigilance |
| **F** — Genomics & Precision Medicine | 6 | Variant calling, tumour genomics, polygenic risk scores |
| **G** — Population Health & Operations | 9 | Claims analytics, surveillance, cybersecurity, agentic workflows |

### Category A — Clinical Diagnostics & Imaging (10 use cases)

The largest regulatory category by volume: 1,104 of 1,451 FDA-cleared AI
devices (76%) are radiology tools. The evidence base within this category
is internally polarised. Mammography AI and colonoscopy polyp detection
have RCT-grade outcome evidence and low deployment. Stroke LVO triage has
both evidence and reimbursement, making it the field's
reimbursement-success benchmark. ECG interpretation spans consumer to
clinical, with AliveCor's 350 million ECG dataset and CMS reimbursement
achieved in 2025 for Kardia 12L. General radiology CAD faces a structural
clearance–adoption gap: despite over 1,100 cleared devices, roughly 30% of
radiologists use AI clinically, held back by absent permanent reimbursement
codes.

### Category B — Clinical Decision Support & Risk Prediction (9 use cases)

The category with the sharpest internal divergence between deployment and
evidence. Sepsis prediction via the Epic Sepsis Model is the canonical
case: deployed at hundreds of hospitals, externally validated at AUC 0.63
with a 67% miss rate. Acute kidney injury prediction, by contrast, achieves
gradient-boosting AUC of 0.87–0.90 at 24–48 hours ahead of onset and has
NHS deployment, but mixed outcome RCTs and no reimbursement. Hospital
readmission prediction is the most quietly scaled non-administrative AI in
healthcare, embedded in 71% of US hospital EHRs. Generative AI for clinical
decision-making remains the category's most overhyped use case: the only
published physician RCT (Goh et al., *JAMA Network Open* 2024) found a
2-percentage-point advantage that did not reach significance.

### Category C — Administrative & Revenue Cycle (5 use cases)

The commercial engine of health AI. Ambient documentation scribes reached
$600 million in spend and deployment in 62.6% of US Epic hospitals by
mid-2025, with a five-centre JAMA study (8,581 clinicians) documenting 16
fewer minutes of documentation per eight patient-hours and a 21% burnout
reduction at Mass General Brigham. RCM AI carries clear ROI signals and is
scaling rapidly toward agentic "touchless" workflows. Prior authorisation
automation is the most contested use case in all of healthcare AI:
simultaneously reducing provider-side denial workloads and generating
documented class-action litigation, state prohibition laws, and an 82%
overturn rate on appealed Medicare Advantage denials. Claims denial appeal
automation is an emerging response to that adversarial dynamic, growing
directly alongside the scribe–coding complex.

### Category D — Patient-Facing & Remote Care (6 use cases)

A category of contrasts between proven remote monitoring and overhyped
chatbots. Remote patient monitoring with AI achieves 23–53% readmission
reductions in heart failure and 7.3 mmHg systolic reductions in large
hypertension cohorts. Wearable AI for atrial fibrillation detection has
consumer-to-clinical scale: the Apple Heart Study enrolled 419,093
participants, and CMS established Medicare payment for Kardia 12L in
hospital outpatient settings in 2025. Mental health chatbots represent the
category's failure case: Woebot closed its consumer app in June 2025 after
1.5 million users, citing unsustainable consumer-model economics, and the
FDA held a November 2025 public meeting on generative mental-health devices
with zero cleared products on the register.

### Category E — Drug Discovery & R&D (5 use cases)

The longest time-horizon category and the most institutionally
underestimated. AlphaFold's 200 million predicted protein structures earned
the 2024 Nobel Prize in Chemistry and are cited in clinical articles at
twice the pre-AlphaFold rate. AI drug discovery attracted $3.3 billion in
venture capital in 2024. The critical caveat remains: **no AI-designed drug
has completed a human clinical trial**, and Isomorphic Labs' first
readouts, initially anticipated in 2025, are now expected by end-2026.
Clinical trial patient-matching is the evidence-strongest sub-use-case: the
RECTIFIER RCT reported near-doubling of enrolment rates, and TrialGPT
(*Nature Communications* 2024) reduced the eligible trial pool by 90% while
achieving 87% eligibility accuracy. Pharmacovigilance AI is a growing but
underrecognized area, with NLP demonstrating superior sensitivity to manual
ADE screening from EHR and social-media data.

### Category F — Genomics & Precision Medicine (6 use cases)

The most operationally mature and publicly invisible category. DeepVariant
for variant calling is deployed at population scale at the NIH All of Us
programme (245,388 participants, 1 billion+ variants), UK Biobank, and
Regeneron, identifying disease-causing variants in 14% more individuals
than prior methods and completing a 30x genome in under 25 minutes on
NVIDIA Parabricks. ArteraAI Prostate, FDA De Novo cleared in August 2025
and NCCN guideline-recommended, has demonstrated utility across four
phase-3 RCTs. AI tumour genomics via liquid biopsy platforms (Foundation
One CDx, Guardant360) has entered clinical standard-of-care in oncology,
particularly NSCLC. Polygenic risk scores remain the category's cautionary
use case: clinical utility is not established in the general population,
and systematic overprediction in non-European ancestries creates
documented equity risk if premature clinical deployment proceeds.

### Category G — Population Health & Operations (9 use cases)

Broad, deeply embedded, and largely ungoverned. Claims analytics,
epidemiological surveillance, supply chain AI, and capacity management
operate at scale in most large health systems without the clinical-evidence
scrutiny applied to device-classified AI. McKinsey estimates current AI
could unlock $60–120 billion per year in hospital savings through
operational efficiency. Cybersecurity AI has scaled rapidly in response to
a 264% increase in healthcare ransomware attacks between 2018 and 2023,
representing an underrated but rapidly growing AI budget line. Agentic AI
for workflow automation is the category's emerging frontier: Epic announced
an agentic suite at its August 2025 Users Group Meeting; Microsoft
introduced healthcare agents at Ignite 2025. Peer-reviewed governance
frameworks for agentic healthcare AI are nascent, with the first systematic
framework publications appearing in 2025–2026.

## Mapping evidence against deployment

All 50 use cases are mapped on the interactive Compass chart below.

- **X axis** — real-world evidence of impact (1–10 scale calibrated to
  study design: 1 = theoretical/no evidence, 5 = single-centre task
  validation, 7 = multi-centre or external validation, 9+ = RCT with
  patient-outcome primary endpoint).
- **Y axis** — deployment and commercial maturity (1 = experimental
  research only, 5 = multi-site pilots, 7 = scaled at health-system level,
  9+ = scaled and formally reimbursed).
- **Bubble size** — estimated 2024–2026 market spend or venture investment
  in USD millions.

**[Explore the interactive visualization on Flourish →](https://public.flourish.studio/visualisation/29302923/)**

## Implications for AI professionals entering healthcare

AI professionals assume the healthcare buyer's primary objection to AI is
clinical evidence, when in most cases the actual blockers are not whether
the model works, but reimbursement pathways, EHR integration, and
institutional/governance liability.

Healthcare presents three distinct value propositions that require three
distinct communication strategies, and conflating them is the most common
vendor error:

1. **Administrative AI** — the primary decision criterion is ROI (driven
   by either cost reduction or risk avoidance) and integration complexity;
   patient-outcome evidence is generally less relevant to the buyer.
2. **Clinical AI targeting FDA or CE clearance** — peer-reviewed external
   validation and a credible reimbursement pathway are necessary but not
   sufficient for adoption; institutional inertia and training costs are
   often the decisive friction.
3. **Research and R&D AI** — credibility comes from publication in
   high-impact journals and academic-medical-centre partnerships, not from
   commercial deployment claims.

The most structurally underserved commercial opportunity in the data is the
**"proven, under-adopted"** quadrant (bottom-right): mammography AI,
colonoscopy CADe (44 positive randomized control trials with no
standard-of-care adoption, per Topol's May 2026 *Lancet* essay), variant
calling, radiotherapy auto-segmentation, and wearable atrial fibrillation
detection each have strong evidence and limited deployment. The barrier is
not clinical utility but reimbursement infrastructure, interoperability,
and institutional trust. Vendors and health system leaders that address the
infrastructure layer (e.g. permanent CPT codes, local validation tooling,
integration support) will capture the most defensible market positions as
the regulatory environment matures.

The **"deployed, disappointing"** (top-left) quadrant carries the most
immediate patient-safety implication and the clearest governance argument.
The Epic Sepsis Model, payer prior-authorisation AI, and Woebot's consumer
mental-health platform all scaled before rigorous independent validation
was conducted at the deployment population.

My recommendation? To health executives: understand this quadrant, then ask
the right validation questions before onboarding future tools, regardless
of vendor-reported performance metrics.

To Health-IT engineers, product managers and entrepreneurs: do not give up,
but keep a strong focus on your business model — who benefits from the
product, who would pay for it, and what accreditations/credentials would
they use as a first filter?

## References

1. The Imaging Wire. *FDA Updates AI List with New Clearances.* March 11,
   2026. 1,451 authorisations through December 2025; 1,104 (76%) radiology.
   [theimagingwire.com](http://theimagingwire.com/)
2. FDA AI/ML-Enabled Medical Devices database (official). Reviewed June
   2026. No LLM or foundation-model-based device cleared as of review date.
   [fda.gov](http://fda.gov/)
3. ONC/AHA. *Hospital Trends in the Use, Evaluation, and Governance of
   Predictive AI, 2023–2024.* ASTP Health IT Data Brief. September 2025.
   71% of US hospitals use predictive AI in EHR.
   [ncbi.nlm.nih.gov](http://ncbi.nlm.nih.gov/)
4. GlobeNewswire / Menlo Ventures. *Healthcare Adopts AI 2.2x Faster Than
   Other Industries, Driving Record $1.4B in AI Spending.* October 21,
   2025. [globenewswire.com](http://globenewswire.com/)
5. Topol E. *The Paradox of Medical AI Implementation.* Ground Truths / The
   Lancet. May 2026. 44 colonoscopy RCTs favour AI; none has reached
   standard-of-care adoption. [erictopol.substack.com](http://erictopol.substack.com/)
6. Rotenstein L, Holmgren J, Thombley R, et al. *Ambient AI Scribes:
   Association with Documentation Time, Efficiency, and Burnout.* JAMA
   Network Open. April 2026. 8,581 clinicians; −16 min EHR/8hrs; −21%
   burnout at MGB. [jamanetwork.com](http://jamanetwork.com/)
7. Health Affairs / AMA / Senate committee documentation. Prior-authorisation
   AI: 82% overturn rate on appealed Medicare Advantage denials; ~75% of
   health plans use AI for PA; CMS WISeR pilot launched January 2026.
8. Hernström V, Josefsson A, Sartor H, et al. *AI-supported screening
   mammography — MASAI trial final results.* The Lancet. February 2026.
   105,934 women; +29% detection; −44.3% workload; no false-positive
   increase.
9. AliveCor press release. *FDA Clearance of New Cardiac Determinations for
   Kardia 12L; 39 Total Cleared Determinations.* January 14, 2026. CMS
   Medicare reimbursement established 2025; 250+ practices; 4,000+
   MI/ischaemia identifications. [alivecor.com](http://alivecor.com/)
10. Sivakumar R, Lue B, Kundu S. *FDA Approval of AI and Machine Learning
    Devices in Radiology.* JAMA Network Open. November 2025. PMC12595527.
    950 devices through June 2024, 76% radiology.
    [pmc.ncbi.nlm.nih.gov](http://pmc.ncbi.nlm.nih.gov/)
11. Wong A, et al. *The Epic Sepsis Model Falls Short.* JAMA Internal
    Medicine. 2021. 27,697 patients; AUC 0.63; sensitivity 33%; PPV 12%;
    67% miss rate. [researchgate.net](http://researchgate.net/)
12. Goh E, Gallo R, Hom J, et al. *Large Language Model Influence on
    Diagnostic Reasoning: A Randomized Clinical Trial.* JAMA Network Open.
    2024;7(10):e2440969. LLM group 76% vs 74%; P=0.60.
13. NIH / DelveInsight RPM review. Heart-failure readmission reductions
    23–53%; hypertension systolic reduction 7.3 mmHg.
    [ncbi.nlm.nih.gov](http://ncbi.nlm.nih.gov/)
14. Woebot Health press release. Consumer app shutdown June 30, 2025. FDA
    public meeting on generative mental-health devices, November 2025;
    zero cleared devices.
15. ISPOR Working Group. *Generative AI in Health Economics: A Taxonomy.*
    arXiv:2410.20204. AlphaFold 2024 Nobel Prize in Chemistry; 200M+
    protein structures. [arxiv.org](http://arxiv.org/)
16. RECTIFIER RCT data; Shi J et al. *TrialGPT.* Nature Communications
    2024. RECTIFIER: ~2x enrolment. TrialGPT: −90% pool, 87.3% accuracy,
    −42.6% screening time.
17. PMC. *Artificial Intelligence in Pharmacovigilance: Toward Real-Time
    Drug-Safety Systems.* PMC12889357. Feb 2026. NLP superior sensitivity
    vs manual ADE screening. [pmc.ncbi.nlm.nih.gov](http://pmc.ncbi.nlm.nih.gov/)
18. Google for Health / NIH All of Us. DeepVariant; All of Us 245,388
    participants; NVIDIA Parabricks <25 min 30x genome.
    [health.google](http://health.google/)
19. European Journal of Human Genetics. *Clinical Implementation of
    Polygenic Risk Scores.* 2025. Clinical utility not established;
    ancestry overprediction in non-European populations.
    [nature.com](http://nature.com/)
20. Healthcare cybersecurity data: 264% increase in ransomware attacks
    2018–2023 (JAMA / HHS data); 40% of large insurers lack AI
    accountability practices (Health Affairs survey). McKinsey $60–120B
    hospital savings estimate. [mckinsey.com](http://mckinsey.com/)
21. arXiv. *Agentic AI Governance and Lifecycle Management in Healthcare.*
    arXiv:2601.15630. 2026. First systematic governance framework for
    healthcare agentic AI. [arxiv.org](http://arxiv.org/)

---

*This article is independent personal work, unrelated to any current or
former employer or client engagement. See [DISCLAIMER.md](../DISCLAIMER.md)
for the full statement.*
