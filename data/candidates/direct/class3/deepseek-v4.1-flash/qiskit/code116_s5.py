# EVAL_META: task_id=116, framework=qiskit, class=3
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import MatrixExponential


def synthesize_evolution_gate(pauli_string, time):
    operator = SparsePauliOp(pauli_string)
    evolution_gate = PauliEvolutionGate(
        operator, time=time, synthesis=MatrixExponential()
    )
    num_qubits = len(pauli_string)
    circuit = QuantumCircuit(num_qubits)
    circuit.append(evolution_gate, range(num_qubits))
    return circuit
