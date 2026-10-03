# EVAL_META: task_id=28, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def visualize_bell_states():
    machine = init_quantum_machine(QMachineType.CPU)
    q1 = machine.qAlloc_many(2)
    c1 = machine.cAlloc_many(2)
    q2 = machine.qAlloc_many(2)
    c2 = machine.cAlloc_many(2)

    phi_plus = QProg()
    phi_plus << H(q1[0]) << CNOT(q1[0], q1[1]) << Measure(q1[0], c1[0]) << Measure(q1[1], c1[1])

    phi_minus = QProg()
    phi_minus << X(q2[0]) << H(q2[0]) << CNOT(q2[0], q2[1]) << Measure(q2[0], c2[0]) << Measure(q2[1], c2[1])

    shots = 1000
    phi_plus_counts = machine.run_with_configuration(phi_plus, c1, shots)
    phi_minus_counts = machine.run_with_configuration(phi_minus, c2, shots)

    phi_plus_total = builtins.sum(phi_plus_counts.values())
    phi_minus_total = builtins.sum(phi_minus_counts.values())

    result = {
        "phi_plus": {k: v / phi_plus_total for k, v in phi_plus_counts.items()},
        "phi_minus": {k: v / phi_minus_total for k, v in phi_minus_counts.items()},
    }

    machine.finalize()
    return result
