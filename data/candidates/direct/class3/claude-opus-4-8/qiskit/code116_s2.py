# EVAL_META: task_id=116, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import MatrixExponential


def synthesize_evolution_gate(pauli_string, time):
    operator = SparsePauliOp.from_list([(pauli_string, 1.0)])
    evo_gate = PauliEvolutionGate(operator, time=time, synthesis=MatrixExponential())
    num_qubits = len(pauli_string)
    circuit = QuantumCircuit(num_qubits)
    circuit.append(evo_gate, range(num_qubits))
    return circuit
