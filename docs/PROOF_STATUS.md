# TenderLens — verified test evidence (26 October 2026)

## Confirmed

- Local isolated logic tests: **39/39 PASS** (Python 3.13.5, GenLayer API stand-in).
- Official GenLayer Direct Mode tests, actual SDK: **5/5 PASS** (Python 3.12.15, genlayer-test 0.29.2).
- Official GenVM linter: **PASS** (3 static checks and SDK validation).
- GenVM typecheck: **PASS** (no type errors).
- GenVM ABI/schema extraction: **PASS** (8 methods, 5 write / 3 view).
- Python source compilation: **PASS**.
- Complete green GitHub workflow: https://github.com/maho0638/tenderlens-genlayer/actions/runs/40310132041
- Source SHA-256 from same green workflow: fcf76c47d5d5970e2711a007b4e1d60809f16173cab19d5d74fd4a0e595458ed
- Source: https://github.com/maho0638/tenderlens-genlayer/blob/main/contracts/tender_lens.py

## Real Studionet proof (2026-10-26)

- **1/1 real Studionet end-to-end integration test PASS**, including deployment and five test transactions, two distinct test account signers, two consensus-backed assessment calls, and RPC readback.
- Contract: `0x3c13B29B72C37c24a5B0CF44ff5dD1c01CF93e0D`.
- Green GitHub network test: https://github.com/maho0638/tenderlens-genlayer/actions/runs/40311855809
- The original decision stayed unchanged after an appeal; both observed verdicts were `UNDETERMINED` (valid fail-closed results, not test failures).
- [Exact transaction hashes, source digest and evidence scope](STUDIONET_PROOF_MANIFEST.json).
- Source digest deployed/tested: `fcf76c47d5d5970e2711a007b4e1d60809f16173cab19d5d74fd4a0e595458ed`.
- Source SHA and exact run commit are documented in manifest. Signed test network transactions were done with ephemeral test accounts, not the user's wallet.

## NOT established

- Separately authenticated finality and validator signature audit independent of GenLayer test runner (not performed).
- Verified authenticity of self-reported evidence, guaranteed AI judgment, security audit, or formal proof.
- Economic security or production readiness; this contract never moves funds.

Test execution and returned on-chain state have been observed, but independent code security audit, financial security and formal verification are **not** established. There is no claim of 100% security.

## Expanded regression test and network verification (26 October 2026)

- Expanded official GenLayer Direct Mode tests: **52/52 PASS**, with 8 invalid-identifier cases, boundary controls, unauthorized actions, replay and double-appeal attempts, hashes, and leader/validator class disagreement.
- Green verification run: https://github.com/maho0638/tenderlens-genlayer/actions/runs/40311400265
- Studionet integration script exercised a test deployment, two independent signers, five state-changing calls, two consensus-backed decisions, hash integrity, and RPC readback; all succeeded in the linked run.
- This network test uses the hosted TEST chain and testing-suite accounts, no production currency or user wallet. No security audit or formal verification is implied.
