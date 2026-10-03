# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import *

def run_bell_state_simulator():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << MeasureAll(q, c)

    shots = 1000
    counts = machine.run_with_configuration(prog, c, shots)
    machine.finalize()

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
