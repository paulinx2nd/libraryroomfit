# Source Provenance

## Collection behavior

No live source is fetched. Room features and use policy are public owner declarations; request requirements and time slots are public requester declarations.

The contract performs no live web request, does not scrape a page, and does not silently claim that a label or URL authenticates its publisher. This avoids validator drift from changing pages. If an application needs live retrieval, that retrieval belongs in a separately reviewed mechanism whose validators independently fetch and normalize the same source.

## Integrity bindings

- Contract source SHA-256: `b7b4b1552d19cfd66b0f5106353296b3cfd10981cd95d873dbdfaa830737a511`
- ABI SHA-256: `16363c7a9e56081daae7711cef8291d5ee0907f75cfe9403ae9f4ec94a9509bf`
- Frozen text and canonical JSON records are hashed inside the contract where the workflow needs a content binding.
- Human-readable source references, when present, are expressly marked unverified.

## Fixture policy

Tests use synthetic public fixtures written for this repository. They are not copied production records and do not represent real people.
