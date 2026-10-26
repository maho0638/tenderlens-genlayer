"""Real GenLayer Direct Mode checks; execute on CI where gltest is installed."""
import json
import pytest

def sample(vm, deploy, alice, bob):
    vm.sender = alice
    c = deploy("contracts/tender_lens.py")
    c.create_tender("RFP1", "Landing page", "Must include an HTTPS URL and accessibility explanation.")
    vm.sender = bob
    c.submit_bid("BID1", "RFP1", "A landing page was delivered", "Unverified screenshots provided.")
    return c

def mocked(vm, label):
    vm.clear_mocks()
    vm.mock_llm(r"(?s).*tender rubric assessor.*", json.dumps({"verdict": label}))

def test_full_lifecycle(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = sample(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.sender = direct_alice
    mocked(direct_vm, "UNDETERMINED")
    assert c.evaluate_bid("BID1") == "UNDETERMINED"
    assert direct_vm.run_validator() is True
    assert json.loads(c.get_decision("BID1", False))["round_number"] == 0
    direct_vm.sender = direct_bob
    c.file_appeal("BID1", "Additional evidence submitted")
    direct_vm.sender = direct_alice
    mocked(direct_vm, "MEETS")
    assert c.resolve_appeal("BID1") == "MEETS"
    assert direct_vm.run_validator() is True
    assert json.loads(c.get_decision("BID1", True))["round_number"] == 1
    assert json.loads(c.get_decision("BID1", False))["verdict"] == "UNDETERMINED"

def test_unauthorized_and_replay(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = sample(direct_vm, direct_deploy, direct_alice, direct_bob)
    with direct_vm.expect_revert("Only tender owner"):
        c.evaluate_bid("BID1")
    direct_vm.sender = direct_alice
    mocked(direct_vm, "MEETS")
    c.evaluate_bid("BID1")
    with direct_vm.expect_revert("already evaluated"):
        c.evaluate_bid("BID1")
    with direct_vm.expect_revert("Only bidder"):
        c.file_appeal("BID1", "spoof")

def test_validator_rejects_disagreeing_class(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = sample(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.sender = direct_alice
    mocked(direct_vm, "MEETS")
    c.evaluate_bid("BID1")
    mocked(direct_vm, "DOES_NOT_MEET")
    assert direct_vm.run_validator() is False

def test_bad_model_output_fails_closed(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = sample(direct_vm, direct_deploy, direct_alice, direct_bob)
    direct_vm.sender = direct_alice
    direct_vm.mock_llm(r"(?s).*tender rubric assessor.*", '{"verdict":"APPROVED"}')
    assert c.evaluate_bid("BID1") == "UNDETERMINED"

def test_duplicate_tender_rejected(direct_vm, direct_deploy, direct_alice):
    direct_vm.sender = direct_alice
    c = direct_deploy("contracts/tender_lens.py")
    c.create_tender("RFP1", "Title", "Written compliance rules.")
    with direct_vm.expect_revert("already exists"):
        c.create_tender("RFP1", "Changed", "Other rules")
