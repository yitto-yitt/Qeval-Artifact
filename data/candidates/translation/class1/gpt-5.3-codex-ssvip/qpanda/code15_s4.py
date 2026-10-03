# EVAL_META: task_id=15, framework=qpanda, class=1
from pyqpanda3.core import *

def noisy_bell():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)

    prog = QProg()
    prog.insert(H(q[0]))
    prog.insert(CNOT(q[0], q[1]))
    prog.insert(Measure(q[0], c[0]))
    prog.insert(Measure(q[1], c[1]))

    shots = 1000
    counts = machine.run_with_configuration(prog, c, shots)

    total = sum(counts.values()) if counts else 1
    probs = {k: v / total for k, v in counts.items()}

    machine.finalize()
    return probs
