# EVAL_META: task_id=47, framework=qpanda2, class=1
import pyqpanda as pq

def random_coin_flip(samples):
    qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = qvm.qAlloc_many(1)
    c = qvm.cAlloc_many(1)
    
    prog = pq.QProg()
    prog << pq.H(q[0])
    prog << pq.Measure(q[0], c[0])
    
    counts = pq.run_with_configuration(prog, qvm, samples)
    total = samples
    
    heads = counts.get('0', 0) / total
    tails = counts.get('1', 0) / total
    
    qvm.finalize()
    
    return {'Heads': heads, 'Tails': tails}
