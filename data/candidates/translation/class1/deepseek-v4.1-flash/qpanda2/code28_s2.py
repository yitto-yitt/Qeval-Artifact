# EVAL_META: task_id=28, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def visualize_bell_states():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    c1 = machine.cAlloc_many(2)
    c2 = machine.cAlloc_many(2)

    phi_plus = QProg()
    phi_plus << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c1[0]) << Measure(q[1], c1[1])

    phi_minus = QProg()
    phi_minus << X(q[0]) << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c2[0]) << Measure(q[1], c2[1])

    shots = 1000
    phi_plus_counts = machine.run_with_configuration(phi_plus, c1, shots)
    phi_minus_counts = machine.run_with_configuration(phi_minus, c2, shots)

    phi_plus_total = builtins.sum(phi_plus_counts.values())
    phi_minus_total = builtins.sum(phi_minus_counts.values())

    return {
        "phi_plus": {key: value / phi_plus_total for key, value in phi_plus_counts.items()},
        "phi_minus": {key: value / phi_minus_total for key, value in phi_minus_counts.items()},
    }
