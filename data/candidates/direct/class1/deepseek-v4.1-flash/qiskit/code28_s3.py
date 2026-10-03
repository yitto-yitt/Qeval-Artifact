# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def _bell_circuit(phi_plus: bool) -> QuantumCircuit:
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    if not phi_plus:
        qc.z(0)
    return qc


def visualize_bell_states():
    phi_plus_probs = Statevector.from_instruction(_bell_circuit(True)).probabilities_dict()
    phi_minus_probs = Statevector.from_instruction(_bell_circuit(False)).probabilities_dict()

    phi_plus_probs = {k: float(v) for k, v in phi_plus_probs.items() if v > 1e-12}
    phi_minus_probs = {k: float(v) for k, v in phi_minus_probs.items() if v > 1e-12}

    return {
        "phi_plus": phi_plus_probs,
        "phi_minus": phi_minus_probs,
    }
