# EVAL_META: task_id=47, framework=qpanda, class=1
import pyqpanda3.core as pq

def random_coin_flip(samples):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(1)
    
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.Measure(q[0], c[0])
    
    result = machine.run_with_configuration(prog, c, samples)
    
    total = sum(result.values())
    if total == 0:
        return {'Heads': 0.5, 'Tails': 0.5}
        
    heads_count = result.get('0', 0)
    tails_count = result.get('1', 0)
    
    machine.finalize()
    
    return {'Heads': heads_count / total, 'Tails': tails_count / total}
