"""Five-validator GLSim flow for semantic room selection."""

import json
from pathlib import Path

from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


def _ok(receipt):
    assert tx_execution_succeeded(receipt), json.dumps(receipt, default=str)


def _context(room_id):
    validators = get_validator_factory().batch_create_mock_validators(
        5,
        mock_llm_response={
            "nondet_exec_prompt": {
                "Choose one eligible library room": json.dumps(
                    {"room_id": room_id, "reason_code": "CAPABILITY_MATCH"}
                )
            }
        },
    )
    return {"validators": [validator.to_dict() for validator in validators]}


def test_five_validator_mutual_booking_flow():
    requester_account, room_account = create_accounts(2)
    factory = get_contract_factory(
        contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "library_room_fit.py"
    )
    deployed = factory.deploy_contract_tx(args=[], account=requester_account, wait_transaction_status=TransactionStatus.FINALIZED)
    _ok(deployed)
    address = extract_contract_address(deployed)
    requester = factory.build_contract(address, account=requester_account)
    room_owner = factory.build_contract(address, account=room_account)
    room_id = f"{str(room_account.address).lower()}:ROOM-A"
    request_id = f"{str(requester_account.address).lower()}:STUDY-1"
    _ok(room_owner.register_room(args=["ROOM-A", 12, "Whiteboard, movable tables, video display, and accessible seating are available.", "Meetings must be educational or civic, supervised, and leave the room in its original condition."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(requester.open_request(args=["STUDY-1", 100, 120, 8, "A study group needs a whiteboard and accessible seating for a structured mathematics workshop."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(requester.match_request(args=[request_id]).transact(transaction_context=_context(room_id), wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(room_owner.room_decision(args=[request_id, True, "The room owner approves this educational use."]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    _ok(requester.confirm_booking(args=[request_id]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    assert requester.matches_booking(args=[request_id, room_id, 100, 120]).call() is True
