# EVAL_META: task_id=28, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QProg, H, X, CNOT, Measure


def visualize_bell_states():
    shots = 1000
    machine = CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(2)
        cbits = machine.cAlloc_many(2)

        phi_plus_prog = QProg()
        phi_plus_prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
        phi_plus_prog << Measure(qubits[0], cbits[0]) << Measure(qubits[1], cbits[1])

        phi_minus_prog = QProg()
        phi_minus_prog << X(qubits[0]) << H(qubits[0]) << CNOT(qubits[0], qubits[1])
        phi_minus_prog << Measure(qubits[0], cbits[0]) << Measure(qubits[1], cbits[1])

        phi_plus_counts = machine.run_with_configuration(phi_plus_prog, cbits, shots)
        phi_minus_counts = machine.run_with_configuration(phi_minus_prog, cbits, shots)

        phi_plus_total = builtins.sum(phi_plus_counts.values())
        phi_minus_total = builtins.sum(phi_minus_counts.values())

        return {
            "phi_plus": {key: value / phi_plus_total for key, value in phi_plus_counts.items()},
            "phi_minus": {key: value / phi_minus_total for key, value in phi_minus_counts.items()},
        }
    finally:
        machine.finalize()
