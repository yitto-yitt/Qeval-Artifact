# EVAL_META: task_id=116, framework=qiskit, class=3
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import MatrixExponential


def synthesize_evolution_gate(pauli_string, time):
    operator = SparsePauliOp.from_list([(pauli_string, 1.0)])
    evolution_gate = PauliEvolutionGate(operator, time=time)
    return MatrixExponential().synthesize(evolution_gate)
