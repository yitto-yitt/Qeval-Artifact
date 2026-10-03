# EVAL_META: task_id=116, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import MatrixExponentialSynthesis


def synthesize_evolution_gate(pauli_string, time):
    operator = SparsePauliOp([pauli_string])
    evolution_gate = PauliEvolutionGate(
        operator, time=time, synthesis=MatrixExponentialSynthesis()
    )
    qc = QuantumCircuit(len(pauli_string))
    qc.append(evolution_gate, range(len(pauli_string)))
    return qc
