# EVAL_META: task_id=47, framework=qpanda, class=1
import pyqpanda3.core as pq

def random_coin_flip(samples):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)
    c = qvm.cAlloc_many(1)
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.Measure(q[0], c[0])
    result = qvm.run_with_configuration(prog, c, samples)
    
    counts = {str(k): v for k, v in result.items()}
    total = sum(counts.values())
    if total == 0:
        return {'Heads': 0.5, 'Tails': 0.5}
    return {
        'Heads': counts.get('0', 0) / total,
        'Tails': counts.get('1', 0) / total
    }
