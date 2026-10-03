# EVAL_META: task_id=116, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import MatrixExponential


def synthesize_evolution_gate(pauli_string, time):
    operator = SparsePauliOp(pauli_string)
    evolution_gate = PauliEvolutionGate(
        operator, time=time, synthesis=MatrixExponential()
    )
    circuit = QuantumCircuit(operator.num_qubits)
    circuit.append(evolution_gate, range(operator.num_qubits))
    return circuit
