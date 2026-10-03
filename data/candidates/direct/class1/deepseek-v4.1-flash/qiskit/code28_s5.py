# EVAL_META: task_id=28, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def _prepare_phi_plus():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    return qc


def _prepare_phi_minus():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.z(0)
    qc.cx(0, 1)
    return qc


def _probabilities(circuit):
    probs = Statevector.from_instruction(circuit).probabilities_dict()
    return {bitstring: float(p) for bitstring, p in probs.items() if p > 1e-12}


def visualize_bell_states():
    return {
        "phi_plus": _probabilities(_prepare_phi_plus()),
        "phi_minus": _probabilities(_prepare_phi_minus()),
    }
