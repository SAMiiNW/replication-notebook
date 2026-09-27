from pathlib import Path
CONTRACT=Path('contracts/contract.py').read_text(encoding='utf-8'); SITE=Path('docs/index.html').read_text(encoding='utf-8')
def test_contract_and_interface_surface():
    for name in ('open_study','submit_replication','challenge_replication','resolve_contest','finalize_unchallenged','get_study'):
        assert 'def '+name in CONTRACT and name in SITE
    assert "status:'FINALIZED'" in SITE and '0x15ba04f276568e7735A701533fFd4972Ed71d09a' in SITE
    assert 'challenge_deadline = now()' in CONTRACT and 'supporting_indexes' in CONTRACT
    assert 'RUN REVIEW DEMO' in SITE and 'createAccount,createClient' in SITE
    assert "result.state!=='FINAL'" in SITE and "result.final_outcome!=='REPRODUCED'" in SITE
    assert SITE.count('createAccount()') == 3
