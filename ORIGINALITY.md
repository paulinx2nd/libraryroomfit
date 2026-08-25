# Originality

## Mechanism fingerprint

The mechanism combines deterministic interval exclusion, semantic selection, room-owner approval, and requester confirmation.

Lifecycle: register room -> open timed request -> deterministic eligibility -> consensus room choice -> room approval -> requester confirmation.

Consensus boundary: Validators choose one room only from the already eligible set and agree on room identifier and reason code.

Settlement boundary: Confirmation appends a booking to the chosen room calendar; overlap checks then exclude it from later requests.

## Review-cohort defense

Names, prompts, labels, and method names are not the basis of the distinction. The actor topology, stored state, allowed transitions, validator decision, and deterministic settlement described above are the reusable mechanism. A full-workspace structural scan is run before publication; its JSON report is retained outside the repository-wide source tree and summarized in `AUDIT.md` after the final pass.
