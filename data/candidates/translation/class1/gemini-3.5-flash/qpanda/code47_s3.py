# EVAL_META: task_id=47, framework=qpanda, class=1
import pyqpanda3.core as pq

def random_coin_flip(samples):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    
    qubits = qvm.qAlloc_many(1)
    cbits = qvm.cAlloc_many(1)
    
    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.Measure(qubits[0], cbits[0])
    
    counts = qvm.run_with_configuration(prog, cbits, samples)
    
    total = sum(counts.values())
    if total == 0:
        total = 1
        
    heads_count = sum(v for k, v in counts.items() if str(k).strip().endswith('0'))
    tails_count = sum(v for k, v in counts.items() if str(k).strip().endswith('1'))
    
    qvm.finalize()
    
    return {'Heads': heads_count / total, 'Tails': tails_count / total}
