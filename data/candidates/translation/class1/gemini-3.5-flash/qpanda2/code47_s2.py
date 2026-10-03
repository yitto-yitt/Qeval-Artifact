# EVAL_META: task_id=47, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def random_coin_flip(samples):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(1)
    
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.Measure(q[0], c[0])
    
    result = machine.run_with_configuration(prog, c, samples)
    
    total = builtins.sum(result.values())
    if total == 0:
        total = samples if samples > 0 else 1
        
    heads_prob = result.get('0', 0) / total
    tails_prob = result.get('1', 0) / total
    
    machine.finalize()
    return {'Heads': heads_prob, 'Tails': tails_prob}
