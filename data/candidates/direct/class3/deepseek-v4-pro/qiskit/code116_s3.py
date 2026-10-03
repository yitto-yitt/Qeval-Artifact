# EVAL_META: task_id=116, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import MatrixExponential


def synthesize_evolution_gate(pauli_string, time):
    """Synthesize an evolution gate for a Pauli string."""
    num_qubits = len(pauli_string)
    operator = SparsePauliOp([pauli_string])
    evo_gate = PauliEvolutionGate(operator, time=time, synthesis=MatrixExponential())
    qc = QuantumCircuit(num_qubits)
    qc.append(evo_gate, range(num_qubits))
    return qc
