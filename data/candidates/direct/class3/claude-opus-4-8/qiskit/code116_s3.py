# EVAL_META: task_id=116, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import MatrixExponential


def synthesize_evolution_gate(pauli_string, time):
    operator = SparsePauliOp.from_list([(pauli_string, 1.0)])
    evo_gate = PauliEvolutionGate(operator, time=time, synthesis=MatrixExponential())
    circuit = QuantumCircuit(len(pauli_string))
    circuit.append(evo_gate, range(len(pauli_string)))
    return circuit.decompose()
