# EVAL_META: task_id=139, framework=qiskit, class=2
from qiskit.quantum_info import DensityMatrix, schmidt_decomposition


def schmidt_test(data, qargs_B):
    return schmidt_decomposition(DensityMatrix(data), qargs_B)
