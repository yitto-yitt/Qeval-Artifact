# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda3.core import *
def random_coin_flip(samples):
    qvm = CPUQVM()
    qvm.initQVM()
    qubits = qvm.qAllocMany(1)
    cbits = qvm.cAllocMany(1)
    prog = QProg()
    prog << H(qubits[0]) << Measure(qubits[0], cbits[0])
    result = qvm.runWithConfiguration(prog, cbits, samples)
    counts = result
    total = sum(counts.values())
    return {'Heads': counts.get('0', 0) / total, 'Tails': counts.get('1', 0) / total}
