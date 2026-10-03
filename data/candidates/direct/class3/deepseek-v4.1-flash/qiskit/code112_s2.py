# EVAL_META: task_id=112, framework=qiskit, class=3
from qiskit.quantum_info import SparsePauliOp
from qiskit.synthesis import LieTrotter, SuzukiTrotter

def create_product_formula_circuit(pauli_strings, times, order, reps):
    op = SparsePauliOp(pauli_strings, coeffs=times)
    if order == 1:
        trotter = LieTrotter(reps=reps)
    else:
        trotter = SuzukiTrotter(order=order, reps=reps)
    return trotter.synthesize(op, time=1.0)
