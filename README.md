# TenderLens — GenLayer Intelligent Contract

TenderLens is a bounded, consensus-reviewed tender rubric assessor. A tender owner publishes an **immutable natural-language rubric**, bidders submit proposals with **self-reported evidence**, validators independently classify the evidence, and the bidder may submit **one appeal** with additional evidence.

## Why GenLayer
Some tender conditions require semantic judgment that deterministic smart contracts cannot evaluate alone. TenderLens uses GenLayer `gl.nondet.exec_prompt` inside `gl.vm.run_nondet_unsafe` and compares the **exact normalized verdict** on the leader and validators: `MEETS`, `DOES_NOT_MEET`, `UNDETERMINED`.

## Workflow
1. Owner: `create_tender(tender_id, title, rubric)`.
2. Bidder: `submit_bid(bid_id, tender_id, proposal, evidence)`.
3. Owner: `evaluate_bid(bid_id)` — immutable first verdict.
4. Bidder: `file_appeal(bid_id, supplemental_evidence)` — once.
5. Owner: `resolve_appeal(bid_id)` — second verdict, original remains.
6. Anyone: `get_tender`, `get_bid`, `get_decision(bid_id, appeal)`.

## Technical limits
All IDs are bounded to 48 alphanumeric, dash or underscore characters. Rubrics and proposals have 1,200-character limits; each evidence statement has 2,000. Stored text is bound to SHA-256 but **self-reported evidence is not fact-checked for authenticity**. Model answers are reduced to three classes and unknown outputs become `UNDETERMINED`. There are no tokens, escrow, payouts, price rankings, or guarantees that a tender owner will resolve a bid.

## Tests and proof boundaries
- 39 local isolated *logic* tests passed on 2026-10-26, exercising a stand-in GenLayer API. This does **not** prove GenVM or Studionet behavior.
- Real GenLayer Direct Mode tests are in `tests/direct/`; see GitHub Actions for whether they actually passed.
- GenVM linter, schema and typing checks run in GitHub Actions.
- No live Studionet Explorer transaction or full consensus receipt is claimed here.

See [proof status](docs/PROOF_STATUS.md).

```bash
python -m pip install -r requirements.txt
python -m pytest tests/direct -q
genvm-lint check contracts/tender_lens.py
genvm-lint typecheck contracts/tender_lens.py
genvm-lint schema contracts/tender_lens.py
```
