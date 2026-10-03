# EVAL_META: task_id=116, framework=qiskit, class=3
from qiskit.quantum_info import Pauli
from qiskit.synthesis import MatrixExponential


def synthesize_evolution_gate(pauli_string, time):
    """Synthesize an evolution gate for a Pauli string using MatrixExponential."""
    pauli = Pauli(pauli_string.upper())
    matrix = pauli.to_matrix(sparse=False)
    return MatrixExponential().synthesize(time * matrix)
