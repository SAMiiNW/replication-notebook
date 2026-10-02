# Steward remediation

| Requirement | Code path | Targeted proof | Status |
| --- | --- | --- | --- |
| A finalized transaction must also have successful execution | `docs/index.html` checks consensus and `txExecutionResultName` | `tests/test_surface.py` | PASS locally |
| The public demo tolerates one transient execution failure | demo-only `maxAttempts=2`; manual writes retain `maxAttempts=1` | `tests/test_surface.py` plus public browser run | PASS live |
| The workflow reaches a canonical final record | `open_study`, `submit_replication`, `challenge_replication`, `get_study` | direct contract tests and public browser lifecycle | PASS live |
| Reviewer-visible evidence is reproducible | pinned protocol, rerun, and audit URLs | `evidence/browser-run.json` | PASS live |
