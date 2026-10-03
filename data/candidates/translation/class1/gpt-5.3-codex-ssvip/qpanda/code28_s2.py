# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import *

def visualize_bell_states():
    shots = 1000

    # phi_plus circuit: H(0) -> CNOT(0,1)
    machine1 = CPUQVM()
    machine1.init_qvm()
    q1 = machine1.qAlloc_many(2)
    c1 = machine1.cAlloc_many(2)
    prog1 = QProg()
    prog1 << H(q1[0]) << CNOT(q1[0], q1[1]) << Measure(q1[0], c1[0]) << Measure(q1[1], c1[1])
    phi_plus_counts = machine1.run_with_configuration(prog1, c1, shots)
    machine1.finalize()

    # phi_minus circuit: X(0) -> H(0) -> CNOT(0,1)
    machine2 = CPUQVM()
    machine2.init_qvm()
    q2 = machine2.qAlloc_many(2)
    c2 = machine2.cAlloc_many(2)
    prog2 = QProg()
    prog2 << X(q2[0]) << H(q2[0]) << CNOT(q2[0], q2[1]) << Measure(q2[0], c2[0]) << Measure(q2[1], c2[1])
    phi_minus_counts = machine2.run_with_configuration(prog2, c2, shots)
    machine2.finalize()

    phi_plus_total = sum(phi_plus_counts.values())
    phi_minus_total = sum(phi_minus_counts.values())

    return {
        "phi_plus": {k: v / phi_plus_total for k, v in phi_plus_counts.items()},
        "phi_minus": {k: v / phi_minus_total for k, v in phi_minus_counts.items()},
    }
