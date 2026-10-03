# EVAL_META: task_id=47, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def random_coin_flip(samples):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(1)
    cbits = qvm.cAlloc_many(1)
    
    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.Measure(qubits[0], cbits[0])
    
    counts = qvm.run_with_configuration(prog, cbits, samples)
    total = builtins.sum(counts.values())
    
    return {'Heads': counts.get('0', 0) / total, 'Tails': counts.get('1', 0) / total}
