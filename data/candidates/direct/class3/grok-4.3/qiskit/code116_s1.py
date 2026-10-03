# EVAL_META: task_id=116, framework=qiskit, class=3
from qiskit.quantum_info import Pauli
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import MatrixExponential

def synthesize_evolution_gate(pauli_string, time):
    pauli = Pauli(pauli_string)
    evo_gate = PauliEvolutionGate(pauli, time=time, synthesis=MatrixExponential())
    return evo_gate.definition
