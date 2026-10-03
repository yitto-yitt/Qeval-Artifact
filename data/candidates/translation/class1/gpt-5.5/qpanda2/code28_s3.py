# EVAL_META: task_id=28, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def visualize_bell_states():
    shots = 1000
    machine = init_quantum_machine(QMachineType.CPU)

    q_phi_plus = machine.qAlloc_many(2)
    c_phi_plus = machine.cAlloc_many(2)
    prog_phi_plus = QProg()
    prog_phi_plus << H(q_phi_plus[0]) << CNOT(q_phi_plus[0], q_phi_plus[1])
    prog_phi_plus << Measure(q_phi_plus[0], c_phi_plus[0]) << Measure(q_phi_plus[1], c_phi_plus[1])
    phi_plus_counts = machine.run_with_configuration(prog_phi_plus, c_phi_plus, shots)

    q_phi_minus = machine.qAlloc_many(2)
    c_phi_minus = machine.cAlloc_many(2)
    prog_phi_minus = QProg()
    prog_phi_minus << X(q_phi_minus[0]) << H(q_phi_minus[0]) << CNOT(q_phi_minus[0], q_phi_minus[1])
    prog_phi_minus << Measure(q_phi_minus[0], c_phi_minus[0]) << Measure(q_phi_minus[1], c_phi_minus[1])
    phi_minus_counts = machine.run_with_configuration(prog_phi_minus, c_phi_minus, shots)

    phi_plus_total = builtins.sum(phi_plus_counts.values())
    phi_minus_total = builtins.sum(phi_minus_counts.values())

    result = {
        "phi_plus": {key: value / phi_plus_total for key, value in phi_plus_counts.items()},
        "phi_minus": {key: value / phi_minus_total for key, value in phi_minus_counts.items()},
    }

    destroy_quantum_machine(machine)
    return result
