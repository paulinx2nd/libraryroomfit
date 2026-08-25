# Reviewer Guide

## Mechanism in one sentence

A reusable room marketplace that deterministically filters capacity and calendar conflicts before validators select the best feature match and both parties approve the booking.

## What consensus actually decides

Validators choose one room only from the already eligible set and agree on room identifier and reason code.

## What code settles afterward

Confirmation appends a booking to the chosen room calendar; overlap checks then exclude it from later requests.

## Why this is distinct

The mechanism combines deterministic interval exclusion, semantic selection, room-owner approval, and requester confirmation.

## Fast review path

1. Confirm the pinned dependency on the first source line.
2. Inspect the custom validator and verify it reruns the substantive task.
3. Trace role checks and terminal-state guards in each write method.
4. Run lint, strict type checking, seven direct tests, and the five-validator integration test.
5. Compare `abi.json` and the StudioNet manifest to the committed source hash.

## Known limitations

Feature descriptions are not physically verified. Calendar correctness covers only bookings stored in this contract, and ambiguous requirements can rotate validators.
