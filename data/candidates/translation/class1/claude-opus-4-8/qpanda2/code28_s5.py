# EVAL_META: task_id=28, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, H, X, CNOT

def visualize_bell_states():
    shots = 1000

    machine_plus = CPUQVM()
    machine_plus.init_qvm()
    qubits_plus = machine_plus.qAlloc_many(2)
    cbits_plus = machine_plus.cAlloc_many(2)
    prog_plus = machine_plus.create_empty_qprog()
    prog_plus << H(qubits_plus[0]) \
              << CNOT(qubits_plus[0], qubits_plus[1]) \
              << machine_plus.get_qstate  # placeholder removed below

    prog_plus = machine_plus.create_empty_qprog()
    prog_plus << H(qubits_plus[0]) << CNOT(qubits_plus[0], qubits_plus[1])
    from pyqpanda import measure_all
    prog_plus << measure_all(qubits_plus, cbits_plus)
    phi_plus_counts = machine_plus.run_with_configuration(prog_plus, cbits_plus, shots)
    machine_plus.finalize()

    machine_minus = CPUQVM()
    machine_minus.init_qvm()
    qubits_minus = machine_minus.qAlloc_many(2)
    cbits_minus = machine_minus.cAlloc_many(2)
    prog_minus = machine_minus.create_empty_qprog()
    prog_minus << X(qubits_minus[0]) << H(qubits_minus[0]) << CNOT(qubits_minus[0], qubits_minus[1])
    prog_minus << measure_all(qubits_minus, cbits_minus)
    phi_minus_counts = machine_minus.run_with_configuration(prog_minus, cbits_minus, shots)
    machine_minus.finalize()

    phi_plus_total = builtins.sum(phi_plus_counts.values())
    phi_minus_total = builtins.sum(phi_minus_counts.values())

    return {
        "phi_plus": {key: value / phi_plus_total for key, value in phi_plus_counts.items()},
        "phi_minus": {key: value / phi_minus_total for key, value in phi_minus_counts.items()},
    }
