# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def _bell_probs(phase_minus: bool = False) -> dict:
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    if phase_minus:
        qc.z(0)

    probs = Statevector.from_instruction(qc).probabilities_dict()
    return {bitstring: round(probability, 10) for bitstring, probability in probs.items()}


def visualize_bell_states() -> dict:
    return {
        "phi_plus": _bell_probs(phase_minus=False),
        "phi_minus": _bell_probs(phase_minus=True),
    }
