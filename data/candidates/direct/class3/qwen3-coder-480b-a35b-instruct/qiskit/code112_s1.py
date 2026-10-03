# EVAL_META: task_id=112, framework=qiskit, class=3

from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import LieTrotter


def create_product_formula_circuit(pauli_strings, times, order, reps):
    # Create a sparse Pauli operator from the pauli strings
    pauli_op = SparsePauliOp(pauli_strings, coeffs=times)
    
    # Create the LieTrotter product formula with specified order and repetitions
    lie_trotter = LieTrotter(reps=reps)
    
    # Synthesize the circuit using the product formula
    circuit = lie_trotter.synthesize(pauli_op)
    
    return circuit
