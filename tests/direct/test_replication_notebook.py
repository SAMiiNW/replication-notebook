from conftest import CONTRACT
import json

PROTOCOL='https://protocol.example/method'; ORIGINAL='https://results.example/original'; REPRO='https://lab.example/rerun'; AUDIT='https://audit.example/rerun'

def opened(vm,deploy,alice,bob,charlie):
    vm.strict_mocks=True; vm.check_pickling=True; vm.warp('2036-01-01T00:00:00+00:00'); vm.sender=alice
    vm.mock_web(r'protocol\.example',{'status':200,'body':'Protocol measures median recovery time in integer milliseconds.'}); vm.mock_web(r'results\.example',{'status':200,'body':'Original median recovery time: 100 milliseconds.'}); vm.mock_llm(r'.*baseline extraction.*','{"protocol_matches":true,"original_value":100,"unit":"ms"}')
    c=deploy(CONTRACT); c.open_study('study-9','0x'+bob.hex(),'0x'+charlie.hex(),'A deterministic recovery routine remains within five percent of the published median.','median recovery time',500,PROTOCOL,ORIGINAL,600); return c

def reproduce(vm,value=103,compliant=True,host='lab'):
    vm.mock_web((r'lab\.example' if host=='lab' else r'audit\.example'),{'status':200,'body':f'Rerun followed protocol. Median recovery time: {value} milliseconds.'}); vm.mock_llm(r'.*reproduction extraction.*',json.dumps({'compliant':compliant,'value':value}))

def test_fresh_challenge_window_and_unchallenged_finalization(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
    c=opened(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie); direct_vm.warp('2036-02-01T00:00:00+00:00'); direct_vm.sender=direct_bob; direct_vm.clear_mocks(); reproduce(direct_vm); c.submit_replication('study-9',REPRO); x=c.get_study('study-9'); assert x['state']=='CHALLENGE_OPEN' and x['challenge_deadline']==2085437400
    with direct_vm.expect_revert('closed unchallenged window required'): c.finalize_unchallenged('study-9')
    direct_vm.warp('2036-02-01T00:10:01+00:00'); direct_vm.sender=direct_alice; c.finalize_unchallenged('study-9'); assert c.get_study('study-9')['final_outcome']=='REPRODUCED'

def test_auditor_contest_and_resolution(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
    c=opened(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie); direct_vm.sender=direct_bob; direct_vm.clear_mocks(); reproduce(direct_vm,103); c.submit_replication('study-9',REPRO); direct_vm.sender=direct_charlie; direct_vm.clear_mocks(); reproduce(direct_vm,125,True,'audit'); c.challenge_replication('study-9',AUDIT); assert c.get_study('study-9')['state']=='CONTESTED'
    direct_vm.clear_mocks(); direct_vm.mock_web(r'lab\.example',{'status':200,'body':'Rerun followed protocol. Median recovery time: 103 milliseconds.'}); direct_vm.mock_web(r'audit\.example',{'status':200,'body':'Rerun followed protocol. Median recovery time: 125 milliseconds.'}); direct_vm.mock_llm(r'.*contest resolution.*','{"outcome":"DIVERGED","value":125,"supporting_indexes":[1]}'); direct_vm.sender=direct_alice; c.resolve_contest('study-9'); assert c.get_study('study-9')['state']=='FINAL' and c.get_study('study-9')['final_outcome']=='DIVERGED'

def test_forged_reproduction_output_is_rejected(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
    c=opened(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie); direct_vm.clear_mocks(); reproduce(direct_vm); result=c._evaluate(c.studies['STUDY-9'],REPRO); assert direct_vm.run_validator(leader_result=result) is True
    forged=dict(result); forged['outcome']='DIVERGED'; assert direct_vm.run_validator(leader_result=forged) is False

def test_unauthorized_and_late_challenges_fail(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
    c=opened(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie); direct_vm.sender=direct_bob; direct_vm.clear_mocks(); reproduce(direct_vm); c.submit_replication('study-9',REPRO); direct_vm.sender=direct_alice; direct_vm.clear_mocks(); reproduce(direct_vm,125,True,'audit')
    with direct_vm.expect_revert('timely auditor challenge'): c.challenge_replication('study-9',AUDIT)
    direct_vm.sender=direct_charlie; direct_vm.warp('2036-01-01T00:10:01+00:00')
    with direct_vm.expect_revert('timely auditor challenge'): c.challenge_replication('study-9',AUDIT)

def test_duplicate_roles_and_origins_fail(direct_vm,direct_deploy,direct_alice,direct_bob):
    direct_vm.sender=direct_alice; c=direct_deploy(CONTRACT)
    with direct_vm.expect_revert('complete independent study registration required'):
        c.open_study('dup','0x'+direct_bob.hex(),'0x'+direct_bob.hex(),'A sufficiently detailed study claim for registration.','median',500,'https://same.example/p','https://same.example/r',600)
