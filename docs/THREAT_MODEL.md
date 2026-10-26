# TenderLens — threat model

- Rubric changed after publishing: no update endpoint; frozen SHA-256 commitment.
- Unauthorized evaluation: only the tender owner's on-chain address may evaluate.
- Duplicate evaluation / double appeal: flags make each action single-use.
- False or manipulated evidence: NOT prevented. All evidence is explicitly bidder self-reported.
- LLM prompt injection: content is bounded and XML-escaped; language models remain vulnerable in principle.
- Non-deterministic disagreement: leader and validators compare the normalized decision class; disagreements reject consensus, not an accepted positive verdict.
- Fraudulent owner: NOT prevented. Owner has sole right to perform evaluations, possibly never.
- Funds: no asset movement. Does not rank by money, execute procurement, or distribute awards.
- Global ID namespace: IDs are globally unique and may be preempted. Bidders should use unpredictable IDs.
- State rent / denial of service: bounded texts; still vulnerable to volume-based on-chain storage growth.

This is a research tool. SHA-256 proves only stable commitment to submitted text, not its accuracy.
