# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def visualize_bell_states():
    def distribution(circuit):
        state = Statevector.from_instruction(circuit)
        probs = state.probabilities_dict()
        return {bits: round(p, 12) for bits, p in probs.items() if p > 0}

    phi_plus = QuantumCircuit(2)
    phi_plus.h(0)
    phi_plus.cx(0, 1)

    phi_minus = QuantumCircuit(2)
    phi_minus.h(0)
    phi_minus.cx(0, 1)
    phi_minus.z(0)

    return {
        "phi_plus": distribution(phi_plus),
        "phi_minus": distribution(phi_minus),
    }
