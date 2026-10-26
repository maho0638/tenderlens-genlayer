"""Public Studionet integration; signs TEST-network transactions only.

Scope: deploy, independent bidder submission, owner consensus evaluation,
bidder appeal, second owner consensus evaluation, immutable hashes and RPC readback.
Not a security audit, mainnet deployment or proof of evidence authenticity.
"""
import hashlib
import json
import pytest
from gltest import get_contract_factory
from gltest.assertions import tx_execution_succeeded


RUBRIC = (
    "The bid must describe a web-based accessibility strategy, including "
    "keyboard navigation and readable text. Evidence must support both."
)
EVIDENCE = (
    "Self-reported demonstration evidence: the bidder says the page supports "
    "keyboard-only navigation. Readability audit evidence has not been submitted."
)
SUPPLEMENT = (
    "Additional self-reported accessibility evidence: the bidder says a "
    "readability review and contrast assessment were completed."
)


def as_record(value):
    return json.loads(str(value))


@pytest.mark.integration
def test_tenderlens_real_studionet_lifecycle(default_account, accounts):
    # A separate signer demonstrates that owner-only operations really require owner.
    bidder = next(
        (acc for acc in accounts
         if str(acc.address).lower() != str(default_account.address).lower()),
        None,
    )
    assert bidder is not None, "A second test account is required"

    factory = get_contract_factory("TenderLens")
    contract = factory.deploy(account=default_account, consensus_max_rotations=4)
    bidder_contract = contract.connect(bidder)
    print("TENDERLENS_CONTRACT=" + str(contract.address), flush=True)
    print("TENDERLENS_OWNER=" + str(default_account.address), flush=True)
    print("TENDERLENS_BIDDER=" + str(bidder.address), flush=True)

    tx = contract.create_tender(args=["PUBLIC-RFP-1", "Accessible web page", RUBRIC]).transact(
        wait_interval=10000, wait_retries=70,
    )
    assert tx_execution_succeeded(tx)
    print("CREATE_TENDER_TX=" + str(tx.get("hash", "")), flush=True)
    tender = as_record(contract.get_tender(args=["PUBLIC-RFP-1"]).call())
    assert tender["owner"].lower() == str(default_account.address).lower()
    assert tender["rubric"] == RUBRIC
    assert tender["rubric_sha256"] == hashlib.sha256(RUBRIC.encode()).hexdigest()

    tx = bidder_contract.submit_bid(args=[
        "BID-1", "PUBLIC-RFP-1",
        "We built a keyboard accessible landing page with legible content.",
        EVIDENCE,
    ]).transact(wait_interval=10000, wait_retries=70)
    assert tx_execution_succeeded(tx)
    print("SUBMIT_BID_TX=" + str(tx.get("hash", "")), flush=True)
    bid_before = as_record(contract.get_bid(args=["BID-1"]).call())
    assert bid_before["bidder"].lower() == str(bidder.address).lower()
    assert bid_before["evaluated"] is False
    assert bid_before["evidence_sha256"] == hashlib.sha256(EVIDENCE.encode()).hexdigest()

    tx = contract.evaluate_bid(args=["BID-1"]).transact(
        consensus_max_rotations=4, wait_interval=10000, wait_retries=100,
    )
    assert tx_execution_succeeded(tx)
    print("FIRST_CONSENSUS_TX=" + str(tx.get("hash", "")), flush=True)
    first = as_record(contract.get_decision(args=["BID-1", False]).call())
    assert first["round_number"] == 0
    assert first["rubric_sha256"] == tender["rubric_sha256"]
    assert first["evidence_sha256"] == bid_before["evidence_sha256"]
    assert first["verdict"] in {"MEETS", "DOES_NOT_MEET", "UNDETERMINED"}
    assert as_record(contract.get_bid(args=["BID-1"]).call())["evaluated"] is True

    tx = bidder_contract.file_appeal(args=["BID-1", SUPPLEMENT]).transact(
        wait_interval=10000, wait_retries=70,
    )
    assert tx_execution_succeeded(tx)
    print("FILE_APPEAL_TX=" + str(tx.get("hash", "")), flush=True)
    bid_after = as_record(contract.get_bid(args=["BID-1"]).call())
    assert bid_after["appeal_filed"] is True
    assert bid_after["appeal_sha256"] == hashlib.sha256(SUPPLEMENT.encode()).hexdigest()

    tx = contract.resolve_appeal(args=["BID-1"]).transact(
        consensus_max_rotations=4, wait_interval=10000, wait_retries=100,
    )
    assert tx_execution_succeeded(tx)
    print("APPEAL_CONSENSUS_TX=" + str(tx.get("hash", "")), flush=True)

    original_after = as_record(contract.get_decision(args=["BID-1", False]).call())
    appealed = as_record(contract.get_decision(args=["BID-1", True]).call())
    assert original_after == first, "The original decision must remain immutable"
    assert appealed["round_number"] == 1
    assert appealed["verdict"] in {"MEETS", "DOES_NOT_MEET", "UNDETERMINED"}
    assert appealed["rubric_sha256"] == tender["rubric_sha256"]
    assert appealed["evidence_sha256"] == hashlib.sha256(
        (EVIDENCE + "\nSUPPLEMENTAL EVIDENCE:\n" + SUPPLEMENT).encode()
    ).hexdigest()
    assert as_record(contract.get_bid(args=["BID-1"]).call())["appeal_resolved"] is True

    print("TENDERLENS_INITIAL_VERDICT=" + first["verdict"], flush=True)
    print("TENDERLENS_APPEAL_VERDICT=" + appealed["verdict"], flush=True)
    print("TENDERLENS_READBACK_OK=true", flush=True)
