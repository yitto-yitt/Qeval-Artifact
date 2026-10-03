# EVAL_META: task_id=116, framework=qiskit, class=3
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import MatrixExponential

def synthesize_evolution_gate(pauli_string: str, time: float):
    """
    Synthesize an evolution gate using MatrixExponential for a given Pauli string and time.
    """
    operator = SparsePauliOp(pauli_string)
    evolution_gate = PauliEvolutionGate(operator, time=time)
    synthesis_algorithm = MatrixExponential()
    circuit = synthesis_algorithm.synthesize(evolution_gate)
    return circuit
