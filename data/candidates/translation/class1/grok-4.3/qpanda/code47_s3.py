# EVAL_META: task_id=47, framework=qpanda, class=1
import pyqpanda3.core as pq

def random_coin_flip(samples):
    qvm = pq.CPUQVM()
    qvm.initQVM()
    qubits = qvm.qAllocMany(1)
    cbits = qvm.cAllocMany(1)
    prog = pq.QProg()
    prog << pq.H(qubits[0]) << pq.Measure(qubits[0], cbits[0])
    result = qvm.run_with_configuration(prog, cbits, samples)
    counts = result
    total = sum(counts.values())
    return {'Heads': counts.get('0', 0) / total, 'Tails': counts.get('1', 0) / total}
