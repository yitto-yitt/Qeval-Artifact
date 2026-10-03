# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import LieTrotter


def create_product_formula_circuit(pauli_strings, times, order, reps):
    hamiltonian = SparsePauliOp.from_list(list(zip(pauli_strings, times)))
    synthesis = LieTrotter(reps=reps, order=order)
    evolution_gate = PauliEvolutionGate(hamiltonian, time=1.0, synthesis=synthesis)
    circuit = QuantumCircuit(hamiltonian.num_qubits)
    circuit.append(evolution_gate, range(hamiltonian.num_qubits))
    return circuit
