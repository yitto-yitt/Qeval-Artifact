# EVAL_META: task_id=47, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def random_coin_flip(samples):
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(1)
    cbits = machine.cAlloc_many(1)
    prog = QProg()
    prog << H(qubits[0]) << Measure(qubits[0], cbits[0])
    counts = machine.run_with_configuration(prog, cbits, samples)
    total = builtins.sum(counts.values())
    return {'Heads': counts.get('0', 0) / total, 'Tails': counts.get('1', 0) / total}
