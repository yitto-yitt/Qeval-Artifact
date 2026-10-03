# EVAL_META: task_id=116, framework=qiskit, class=3

from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis.evolution import MatrixExponential

def synthesize_evolution_gate(pauli_string, time):
    operator = SparsePauliOp(pauli_string)
    evolution_gate = PauliEvolutionGate(operator, time)
    circuit = MatrixExponential().synthesize(evolution_gate)
    return circuit
