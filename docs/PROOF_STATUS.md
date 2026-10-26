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

## NOT established

- Live Studionet deployment or transaction readback (not performed).
- Finalized independent on-chain validator votes and Explorer receipts (not performed).
- Verified authenticity of self-reported evidence, guaranteed AI judgment, security audit, or formal proof.
- Economic security or production readiness; this contract never moves funds.

This technical evidence applies to the stated test scope only. No claim of 100% security is made.
