"""Direct tests for room eligibility and mutual booking."""

import json


FEATURES = "Whiteboard, movable tables, video display, and accessible seating are available."
POLICY = "Meetings must be educational or civic, supervised, and leave the room in its original condition."
REQUIREMENTS = "A study group needs a whiteboard and accessible seating for a structured mathematics workshop."


def _room(contract, direct_vm, owner, key, capacity=12):
    direct_vm.sender = owner
    return contract.register_room(key, capacity, FEATURES, POLICY)


def _request(contract, direct_vm, requester, key="STUDY-1", start=100, end=120, attendees=8):
    direct_vm.sender = requester
    return contract.open_request(key, start, end, attendees, REQUIREMENTS)


def _match(contract, direct_vm, requester, request_id, room_id):
    direct_vm.sender = requester
    direct_vm.mock_llm(
        r".*Choose one eligible library room.*",
        json.dumps({"room_id": room_id, "reason_code": "CAPABILITY_MATCH"}),
    )
    return contract.match_request(request_id)


def test_room_registration_and_owner_toggle(contract, direct_vm, direct_bob):
    room_id = _room(contract, direct_vm, direct_bob, "ROOM-A")
    contract.set_room_active(room_id, False)
    assert contract.get_room(room_id)["active"] is False


def test_request_rejects_invalid_window(contract, direct_vm, direct_alice):
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("invalid_time_window"):
        contract.open_request("BAD", 20, 20, 4, REQUIREMENTS)


def test_match_approval_and_confirmation_reserve_calendar(contract, direct_vm, direct_alice, direct_bob):
    room_id = _room(contract, direct_vm, direct_bob, "ROOM-A")
    request_id = _request(contract, direct_vm, direct_alice)
    assert _match(contract, direct_vm, direct_alice, request_id, room_id) == room_id
    direct_vm.sender = direct_bob
    assert contract.room_decision(request_id, True, "The room owner approves this use.") == "ROOM_APPROVED"
    direct_vm.sender = direct_alice
    contract.confirm_booking(request_id)
    assert contract.get_request(request_id)["state"] == "CONFIRMED"
    assert contract.room_is_free(room_id, 110, 130) is False


def test_wrong_room_owner_cannot_approve(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    room_id = _room(contract, direct_vm, direct_bob, "ROOM-A")
    request_id = _request(contract, direct_vm, direct_alice)
    _match(contract, direct_vm, direct_alice, request_id, room_id)
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("only_selected_room_owner"):
        contract.room_decision(request_id, True, "Unauthorized approval attempt.")


def test_declined_room_cannot_be_confirmed(contract, direct_vm, direct_alice, direct_bob):
    room_id = _room(contract, direct_vm, direct_bob, "ROOM-A")
    request_id = _request(contract, direct_vm, direct_alice)
    _match(contract, direct_vm, direct_alice, request_id, room_id)
    direct_vm.sender = direct_bob
    contract.room_decision(request_id, False, "The planned use conflicts with room policy.")
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("room_not_approved"):
        contract.confirm_booking(request_id)


def test_calendar_conflict_removes_only_room(contract, direct_vm, direct_alice, direct_bob):
    room_id = _room(contract, direct_vm, direct_bob, "ROOM-A")
    first = _request(contract, direct_vm, direct_alice, "FIRST", 100, 120)
    _match(contract, direct_vm, direct_alice, first, room_id)
    direct_vm.sender = direct_bob
    contract.room_decision(first, True, "Approved for the requested period.")
    direct_vm.sender = direct_alice
    contract.confirm_booking(first)
    second = _request(contract, direct_vm, direct_alice, "SECOND", 110, 125)
    with direct_vm.expect_revert("no_eligible_room"):
        contract.match_request(second)


def test_model_cannot_choose_unknown_room(contract, direct_vm, direct_alice, direct_bob):
    _room(contract, direct_vm, direct_bob, "ROOM-A")
    request_id = _request(contract, direct_vm, direct_alice)
    direct_vm.sender = direct_alice
    direct_vm.mock_llm(
        r".*Choose one eligible library room.*",
        json.dumps({"room_id": "0xdead:UNKNOWN", "reason_code": "CAPABILITY_MATCH"}),
    )
    with direct_vm.expect_revert("ineligible_room"):
        contract.match_request(request_id)
    assert contract.get_request(request_id)["state"] == "OPEN"
