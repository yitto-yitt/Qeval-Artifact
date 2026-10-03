# EVAL_META: task_id=28, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def visualize_bell_states():
    machine = init_quantum_machine(QMachineType.CPU)
    try:
        shots = 1000

        q_plus = machine.qAlloc_many(2)
        c_plus = machine.cAlloc_many(2)
        phi_plus_prog = QProg()
        phi_plus_prog << H(q_plus[0]) << CNOT(q_plus[0], q_plus[1])
        phi_plus_prog << Measure(q_plus[0], c_plus[0]) << Measure(q_plus[1], c_plus[1])
        phi_plus_counts = run_with_configuration(phi_plus_prog, c_plus, shots)

        q_minus = machine.qAlloc_many(2)
        c_minus = machine.cAlloc_many(2)
        phi_minus_prog = QProg()
        phi_minus_prog << X(q_minus[0]) << H(q_minus[0]) << CNOT(q_minus[0], q_minus[1])
        phi_minus_prog << Measure(q_minus[0], c_minus[0]) << Measure(q_minus[1], c_minus[1])
        phi_minus_counts = run_with_configuration(phi_minus_prog, c_minus, shots)

        phi_plus_total = builtins.sum(phi_plus_counts.values())
        phi_minus_total = builtins.sum(phi_minus_counts.values())

        return {
            "phi_plus": {key: value / phi_plus_total for key, value in phi_plus_counts.items()},
            "phi_minus": {key: value / phi_minus_total for key, value in phi_minus_counts.items()},
        }
    finally:
        finalize()
