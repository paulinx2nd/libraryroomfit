# LibraryRoomFit

A reusable room marketplace that deterministically filters capacity and calendar conflicts before validators select the best feature match and both parties approve the booking.

## Why GenLayer

Validators choose one room only from the already eligible set and agree on room identifier and reason code. Confirmation appends a booking to the chosen room calendar; overlap checks then exclude it from later requests.

## Roles

- requester
- room owner
- GenLayer validators

## Lifecycle

register room -> open timed request -> deterministic eligibility -> consensus room choice -> room approval -> requester confirmation

## Contract interface

- Constructor: none
- Write methods: cancel_booking, confirm_booking, match_request, open_request, register_room, room_decision, set_room_active
- View methods: get_request, get_request_count, get_room, matches_booking, room_is_free
- Runner: `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

## Public-data warning

All contract inputs, evidence, notes, addresses, model results, and state are public. Do not submit secrets, private documents, personal contact information, or confidential identifiers.

## Source model

No live source is fetched. Room features and use policy are public owner declarations; request requirements and time slots are public requester declarations.

## Verification

```text
genvm-lint check contracts/library_room_fit.py
genvm-lint typecheck contracts/library_room_fit.py --strict
python -m pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5 --no-browser
python -m pytest tests/integration -q -s
```

The repository contains seven direct tests and one full five-validator GLSim flow. StudioNet evidence is recorded separately under `deployments/` after network execution.

## Limitations

Feature descriptions are not physically verified. Calendar correctness covers only bookings stored in this contract, and ambiguous requirements can rotate validators.

Licensed under MIT. See `LICENSE`.
