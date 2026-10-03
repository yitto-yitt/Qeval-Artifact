# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import LieTrotter

def create_product_formula_circuit(pauli_strings, times, order, reps):
    hamiltonian = SparsePauliOp(pauli_strings, coeffs=times)
    num_qubits = hamiltonian.num_qubits
    synthesis = LieTrotter(reps=reps)
    evolution_gate = PauliEvolutionGate(hamiltonian, time=1.0, synthesis=synthesis)
    qc = QuantumCircuit(num_qubits)
    qc.append(evolution_gate, range(num_qubits))
    return qc.decompose()
