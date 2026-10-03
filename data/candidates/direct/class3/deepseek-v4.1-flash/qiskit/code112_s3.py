# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import LieTrotter

def create_product_formula_circuit(pauli_strings, times, order, reps):
    hamiltonian = SparsePauliOp(pauli_strings, coeffs=times)
    trotter = LieTrotter(order=order, reps=reps)
    return trotter.synthesize(hamiltonian, time=1.0)
