# Audit Record

Audit date: 2026-08-25

## Automated results

- GenVM lint and SDK validation: PASS
- Strict Pyright through genvm-lint: PASS
- Direct-mode tests: 7 PASS
- Five-validator GLSim integration: 1 PASS
- ABI regenerated from final source: PASS
- Pinned runner header: PASS
- Dependency vulnerability audit: PASS, zero known vulnerabilities
- Full-workspace structural originality scan: PASS, 121 contracts scanned; every nearest external match is below 0.35 and has a different public method shape
- StudioNet: PASS - fresh owner-isolated wallets, all transactions finalized and executed successfully, deployed source/schema matched, and mechanism-specific bound state read back
- GitHub publication: PASS - private remote and clean one-commit reachable history verified

## Artifact hashes

- Source: `b7b4b1552d19cfd66b0f5106353296b3cfd10981cd95d873dbdfaa830737a511`
- ABI: `16363c7a9e56081daae7711cef8291d5ee0907f75cfe9403ae9f4ec94a9509bf`

## Manual findings

The substantive validator independently reruns the task. The contract documents caller-attested source limitations, public-data exposure, role boundaries, terminal states, and residual risk. The mechanism combines deterministic interval exclusion, semantic selection, room-owner approval, and requester confirmation. The StudioNet manifest records the contract address, transaction receipts, fresh public test roles, exact source and schema readback, and the mechanism-specific terminal assertion.
