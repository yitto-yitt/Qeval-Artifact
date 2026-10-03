# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import *

def and_gate(a, b):
    init_quantum_machine(QMachineType.SIMULATOR)
    try:
        q = qAlloc_many(9)
        c = cAlloc_many(3)

        a_q = [q[i] for i in range(3)]
        b_q = [q[i] for i in range(3, 6)]
        anc_q = [q[i] for i in range(6, 9)]

        prog = QProg()

        for i in range(3):
            if (a >> i) & 1:
                prog << X(a_q[i])
            if (b >> i) & 1:
                prog << X(b_q[i])

        for i in range(3):
            prog << Toffoli(a_q[i], b_q[i], anc_q[i])

        for i in range(3):
            prog << Measure(anc_q[i], c[i])

        counts = run_with_configuration(prog, c, 1024)
        total = sum(counts.values())
        return {key: value / total for key, value in counts.items() if value > 0}
    finally:
        destroy_quantum_machine()
