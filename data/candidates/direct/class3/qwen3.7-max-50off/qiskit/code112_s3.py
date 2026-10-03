# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit.synthesis import LieTrotter
from qiskit.quantum_info import SparsePauliOp


def create_product_formula_circuit(pauli_strings, times, order, reps):
    op = SparsePauliOp(pauli_strings, times)
    trotter = LieTrotter(reps=reps)
    circuit = trotter.synthesize(op)
    return circuit
