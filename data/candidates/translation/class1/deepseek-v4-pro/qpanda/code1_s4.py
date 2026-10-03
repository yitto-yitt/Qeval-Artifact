# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import *

def run_bell_state_simulator():
    init(QMachineType.CPU)
    q = qAlloc_many(2)
    c = cAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])
    counts = run_with_configuration(prog, c, 1000)
    destroyQuantumMachine()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
