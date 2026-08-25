# Architecture

## Boundary

- Frontend or backend: wallet UX, indexing, private drafts, non-authoritative previews, notifications, and optional off-chain source retrieval.
- GenLayer contract: Validators choose one room only from the already eligible set and agree on room identifier and reason code. Confirmation appends a booking to the chosen room calendar; overlap checks then exclude it from later requests.
- External world: No live source is fetched. Room features and use policy are public owner declarations; request requirements and time slots are public requester declarations.

## Event path

register room -> open timed request -> deterministic eligibility -> consensus room choice -> room approval -> requester confirmation

## Actors

- requester
- room owner
- GenLayer validators

## Consensus design

The leader produces a normalized bounded result. Each validator independently reruns the substantive task from the same frozen public inputs. Validators compare the decision fields that change state, not merely JSON shape. Invalid model output raises `[LLM_ERROR]` so a broken leader is not accepted.

## Deterministic layer

Confirmation appends a booking to the chosen room calendar; overlap checks then exclude it from later requests. Identifiers, bounds, access checks, ordering, counters, masks, hashes, and terminal-state guards are computed deterministically.

## Persistence

State uses GenLayer storage types only. Public composite records are serialized as canonical JSON where appropriate. Source SHA-256 at evidence generation: `b7b4b1552d19cfd66b0f5106353296b3cfd10981cd95d873dbdfaa830737a511`.
