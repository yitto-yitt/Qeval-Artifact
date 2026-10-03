# EVAL_META: task_id=28, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def visualize_bell_states():
    shots = 1000

    # phi_plus circuit
    qvm1 = CPUQVM()
    qvm1.init_qvm()
    q1 = qvm1.qAlloc_many(2)
    c1 = qvm1.cAlloc_many(2)

    prog1 = QProg()
    prog1 << H(q1[0]) << CNOT(q1[0], q1[1]) << Measure(q1[0], c1[0]) << Measure(q1[1], c1[1])

    counts1 = qvm1.run_with_configuration(prog1, c1, shots)
    total1 = builtins.sum(counts1.values())
    phi_plus_probs = {k: v / total1 for k, v in counts1.items()}
    qvm1.finalize()

    # phi_minus circuit
    qvm2 = CPUQVM()
    qvm2.init_qvm()
    q2 = qvm2.qAlloc_many(2)
    c2 = qvm2.cAlloc_many(2)

    prog2 = QProg()
    prog2 << X(q2[0]) << H(q2[0]) << CNOT(q2[0], q2[1]) << Measure(q2[0], c2[0]) << Measure(q2[1], c2[1])

    counts2 = qvm2.run_with_configuration(prog2, c2, shots)
    total2 = builtins.sum(counts2.values())
    phi_minus_probs = {k: v / total2 for k, v in counts2.items()}
    qvm2.finalize()

    return {
        "phi_plus": phi_plus_probs,
        "phi_minus": phi_minus_probs,
    }
