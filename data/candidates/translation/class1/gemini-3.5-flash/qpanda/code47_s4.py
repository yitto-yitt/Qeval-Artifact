# EVAL_META: task_id=47, framework=qpanda, class=1
import pyqpanda3.core as pq

def random_coin_flip(samples):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(1)
    cbits = qvm.cAlloc_many(1)
    
    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.Measure(qubits[0], cbits[0])
    
    result = qvm.run_with_configuration(prog, cbits, samples)
    
    heads_count = result.get('0', 0) + result.get(0, 0)
    tails_count = result.get('1', 0) + result.get(1, 0)
    total = heads_count + tails_count
    
    if total == 0:
        return {'Heads': 0.5, 'Tails': 0.5}
    return {'Heads': heads_count / total, 'Tails': tails_count / total}
