# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import *

def run_bell_state_simulator():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])

    shots = 1000
    counts = qvm.run_with_configuration(prog, c, shots)
    qvm.finalize_qvm()

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
