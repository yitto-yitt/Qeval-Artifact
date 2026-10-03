# EVAL_META: task_id=28, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def visualize_bell_states():
    qvm = init_quantum_machine(QMachineType.CPU)
    try:
        qubits = qvm.qAlloc_many(2)
        cbits = qvm.cAlloc_many(2)
        shots = 1000

        phi_plus_prog = QProg()
        phi_plus_prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
        phi_plus_prog << measure_all(qubits, cbits)

        phi_minus_prog = QProg()
        phi_minus_prog << X(qubits[0]) << H(qubits[0]) << CNOT(qubits[0], qubits[1])
        phi_minus_prog << measure_all(qubits, cbits)

        phi_plus_counts = qvm.run_with_configuration(phi_plus_prog, cbits, shots)
        phi_minus_counts = qvm.run_with_configuration(phi_minus_prog, cbits, shots)

        phi_plus_total = builtins.sum(phi_plus_counts.values())
        phi_minus_total = builtins.sum(phi_minus_counts.values())

        return {
            "phi_plus": {key: value / phi_plus_total for key, value in phi_plus_counts.items()},
            "phi_minus": {key: value / phi_minus_total for key, value in phi_minus_counts.items()},
        }
    finally:
        destroy_quantum_machine(qvm)
