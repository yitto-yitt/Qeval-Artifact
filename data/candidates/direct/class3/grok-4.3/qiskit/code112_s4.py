# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import LieTrotter

def create_product_formula_circuit(pauli_strings, times, order, reps):
    pauli_list = [(pauli_strings[i], times[i]) for i in range(len(pauli_strings))]
    hamiltonian = SparsePauliOp.from_list(pauli_list)
    num_qubits = hamiltonian.num_qubits
    gate = PauliEvolutionGate(hamiltonian, time=1.0, synthesis=LieTrotter(reps=reps))
    circuit = QuantumCircuit(num_qubits)
    circuit.append(gate, range(num_qubits))
    return circuit.decompose()
