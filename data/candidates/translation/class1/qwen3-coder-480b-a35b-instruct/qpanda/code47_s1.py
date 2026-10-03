# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda import *

def random_coin_flip(samples):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(1)
    cbits = qvm.cAlloc_many(1)
    prog = QProg()
    prog.insert(H(qubits[0]))
    prog.insert(Measure(qubits[0], cbits[0]))
    result = qvm.run_with_configuration(prog, cbits, samples)
    counts = result
    total = sum(counts.values())
    return {'Heads': counts.get('0', 0) / total, 'Tails': counts.get('1', 0) / total}
