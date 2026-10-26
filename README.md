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

## Verified tests and hosted Studionet proof — 26 October 2026

- Official GenLayer Direct Mode tests: **52/52 PASS** (authorization, idempotence, hash commitments, invalid inputs, appeals, validator agreement/disagreement, suspicious evidence).
- GenVM lint, SDK, schema and typechecking: **PASS**.
- **Real hosted Studionet test: PASS** — deployed TenderLens with two distinct test accounts, executed five writes (including two consensus-backed assessments), and confirmed original decision, appeal and SHA-256 commitments through RPC readback.
- Studionet contract address: `0x3c13B29B72C37c24a5B0CF44ff5dD1c01CF93e0D`.
- [Successful GitHub network proof](https://github.com/maho0638/tenderlens-genlayer/actions/runs/40311855809) · [Detailed proof manifest](docs/STUDIONET_PROOF_MANIFEST.json) · [Proof status and limitations](docs/PROOF_STATUS.md).
- The two live model verdicts were both `UNDETERMINED`, correctly stored and read back. The system does not authenticate bidder evidence or guarantee model judgments.
- No mainnet deployment, token escrow, production claim, external security audit, or formal verification is implied.

### Run independently

For fast isolated testing:


```bash
python -m pip install -r requirements.txt
python -m pytest tests/direct -q
genvm-lint check contracts/tender_lens.py
genvm-lint typecheck contracts/tender_lens.py
genvm-lint schema contracts/tender_lens.py
```
