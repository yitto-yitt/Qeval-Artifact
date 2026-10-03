# EVAL_META: task_id=116, framework=qiskit, class=3
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import Pauli
from qiskit.synthesis import MatrixExponential


def synthesize_evolution_gate(pauli_string, time):
    synthesis = MatrixExponential()
    gate = PauliEvolutionGate(
        Pauli(pauli_string), time=time, synthesis=synthesis
    )
    return synthesis.synthesize(gate)
