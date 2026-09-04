# score.py — portfolio scorer

Implements the deterministic composite score, the dependency-adjusted value
for enablers, and the rank-stability Monte Carlo test from the
[Use Case Prioritisation Model](../README.md) (Framework 02).

**This tool implements the model. It does not replace the panel.** It
processes scores and evidence grades a cross-functional panel has already
agreed, using the scoring rubric in [`../template/scoring-rubric.md`](../template/scoring-rubric.md).
It does not generate judgements of its own.

## Running it

```bash
pip install -r requirements.txt
python3 score.py portfolio.csv
```

Optional flags:

```bash
python3 score.py portfolio.csv --iterations 10000 --seed 42
```

- `--iterations` — number of Monte Carlo draws (default 10,000, per §1.9).
- `--seed` — random seed, for a reproducible run.

Input is a portfolio register CSV in the format of
[`../template/portfolio-register.csv`](../template/portfolio-register.csv).
See [`../examples/sample-portfolio.csv`](../examples/sample-portfolio.csv)
for a filled, synthetic example.

## What the output means

**Portfolio score table** — for each candidate: the median composite score
across all Monte Carlo iterations, the 10th–90th percentile range, the
proportion of iterations in which it lands in the top quartile of the
portfolio (`P(TopQ)`), its evidence-grade confidence index, and its band.

**Bands**, per §1.9:

- **Robustly prioritised** — P(top quartile) > 0.75. Fund it.
- **Contested** — 0.25–0.75. The model cannot separate these from their
  neighbours; the decision is a judgement call, and should be made and
  minuted as one.
- **Robustly deprioritised** — P(top quartile) < 0.25. Say no, and say why.

No hard rank is published, deliberately. See the framework README and
[`../reference/rank-stability.md`](../reference/rank-stability.md) for why
a point rank claims more precision than the underlying evidence supports.

**Validation warnings** — non-fatal flags raised after scoring: enablers
scoring below the portfolio median (check the minimum enabler allocation
policy before letting the score alone decide), candidates whose Value axis
is graded predominantly D–E (discovery-sprint-only, per §1.7 rule 1, not
buildable on this evidence), and candidates that depend on another
candidate which is not itself in the "Robustly prioritised" band (an unmet
dependency).

## What "runs clean" means

A clean run (exit code 0) means the input passed validation — every score
is an integer 1–5, every grade is A–E, every `depends_on` reference
resolves, and there are no dependency cycles. It does **not** mean the
portfolio is problem-free: a clean run can and typically will still print
validation warnings (an unmet dependency, a discovery-only candidate, an
underperforming enabler) in its third output section. Fatal errors —
malformed input — are printed to stderr and exit non-zero; nothing else is.
