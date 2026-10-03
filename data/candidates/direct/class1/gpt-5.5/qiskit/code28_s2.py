# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def visualize_bell_states():
    phi_plus = QuantumCircuit(2)
    phi_plus.h(0)
    phi_plus.cx(0, 1)

    phi_minus = QuantumCircuit(2)
    phi_minus.h(0)
    phi_minus.cx(0, 1)
    phi_minus.z(0)

    return {
        "phi_plus": Statevector.from_instruction(phi_plus).probabilities_dict(),
        "phi_minus": Statevector.from_instruction(phi_minus).probabilities_dict(),
    }
