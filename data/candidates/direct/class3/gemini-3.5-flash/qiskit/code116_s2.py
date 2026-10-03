# EVAL_META: task_id=116, framework=qiskit, class=3

from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import MatrixExponential

def synthesize_evolution_gate(pauli_string: str, time: float) -> QuantumCircuit:
    """Synthesize an evolution gate using MatrixExponential for a given Pauli string and time.

    Args:
        pauli_string (str): The Pauli string (e.g., 'XYZ').
        time (float): The evolution time.

    Returns:
        QuantumCircuit: The synthesized quantum circuit.
    """
    operator = SparsePauliOp(pauli_string)
    gate = PauliEvolutionGate(operator, time=time)
    synthesizer = MatrixExponential()
    circuit = synthesizer.synthesize(gate)
    return circuit
