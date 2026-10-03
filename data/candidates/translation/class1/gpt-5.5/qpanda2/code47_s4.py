# EVAL_META: task_id=47, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QProg, H, Measure

def random_coin_flip(samples):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(1)
    cbits = qvm.cAlloc_many(1)

    prog = QProg()
    prog << H(qubits[0]) << Measure(qubits[0], cbits[0])

    counts = qvm.run_with_configuration(prog, cbits, samples)
    total = builtins.sum(counts.values())

    qvm.finalize()
    return {'Heads': counts.get('0', 0) / total, 'Tails': counts.get('1', 0) / total}
