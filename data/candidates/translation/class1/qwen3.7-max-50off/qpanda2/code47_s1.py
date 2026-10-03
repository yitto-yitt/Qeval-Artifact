# EVAL_META: task_id=47, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def random_coin_flip(samples):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)
    c = qvm.cAlloc_many(1)
    
    prog = pq.QProg()
    prog << pq.H(q[0])
    prog << pq.Measure(q[0], c[0])
    
    result = qvm.run_with_configuration(prog, c, samples)
    
    total = builtins.sum(result.values())
    
    p_heads = result.get('0', 0) / total
    p_tails = result.get('1', 0) / total
    
    qvm.finalize()
    
    return {'Heads': p_heads, 'Tails': p_tails}
