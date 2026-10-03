# EVAL_META: task_id=139, framework=qiskit, class=2
from qiskit.quantum_info import schmidt_decomposition

def schmidt_test(data, qargs_B):
    coeffs, vecs = schmidt_decomposition(data, qargs_B)
    return [(coeffs[i], vecs[i][0], vecs[i][1]) for i in range(len(coeffs))]
