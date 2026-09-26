# Replication Notebook

Open the protocol. Write down the original number. Hand the notebook to somebody else.

This contract records whether an independent rerun reproduces a published result within a declared numeric tolerance. The protocol and original result are fetched and frozen first. A named rerunner later submits a public artifact. Validators verify protocol compliance, extract the exact metric, and derive the outcome from the stored baseline rather than from prose supplied by the caller.

The challenge clock starts only after the rerun has been assessed. A named auditor gets the full promised window even when the rerun arrives late. Matching audit and rerun outcomes close the notebook immediately. A conflicting audit opens a contest over two hash-pinned artifacts; GenLayer resolves that contest into one final structured outcome.

## Notebook states

`OPEN → CHALLENGE_OPEN → FINAL`

or

`OPEN → CHALLENGE_OPEN → CONTESTED → FINAL`

Anyone may finalize an unchallenged rerun after the protected window. Only the named rerunner can submit the first artifact, and only the named auditor can challenge it.

## What is preserved

- exact protocol and original-result response digests;
- the original signed integer value and short unit;
- reproduction and audit URLs, digests, extracted values, and classifications;
- numeric tolerance and derived basis-point delta;
- a final outcome limited to `REPRODUCED`, `DIVERGED`, or `INVALID`.

The bundled records are operator-created fixtures for a reproducible demonstration. Wallet separation does not make them independent scientific authorities.

## Run the checks

```text
python -X utf8 -m genvm_linter.cli contracts/contract.py
python -m pytest -q tests/test_surface.py -p no:cacheprovider
gltest tests/direct -v
```

Deployment and live-run identifiers are added only after StudioNet finalization.
