# EVAL_META: task_id=116, framework=qiskit, class=3
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import Pauli
from qiskit.synthesis.evolution import MatrixExponential


def synthesize_evolution_gate(pauli_string, time):
    evolution_gate = PauliEvolutionGate(Pauli(pauli_string), time=time)
    return MatrixExponential().synthesize(evolution_gate)
