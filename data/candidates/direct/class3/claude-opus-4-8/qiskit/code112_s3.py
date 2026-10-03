# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import LieTrotter


def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    operator = SparsePauliOp(pauli_strings, coeffs=times)
    synthesis = LieTrotter(reps=reps)
    evolution_gate = PauliEvolutionGate(operator, time=1.0, synthesis=synthesis)
    circuit = QuantumCircuit(num_qubits)
    circuit.append(evolution_gate, range(num_qubits))
    return circuit
