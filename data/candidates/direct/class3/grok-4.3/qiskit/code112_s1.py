# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import LieTrotter

def create_product_formula_circuit(pauli_strings, times, order, reps):
    hamiltonian = SparsePauliOp(pauli_strings, coeffs=times)
    num_qubits = hamiltonian.num_qubits
    synthesis = LieTrotter(reps=reps)
    evo_gate = PauliEvolutionGate(hamiltonian, time=1.0, synthesis=synthesis)
    circuit = QuantumCircuit(num_qubits)
    circuit.append(evo_gate, range(num_qubits))
    return circuit.decompose()
