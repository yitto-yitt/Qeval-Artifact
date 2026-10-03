# EVAL_META: task_id=139, framework=qiskit, class=2
from qiskit.quantum_info import DensityMatrix, schmidt_decomposition


def schmidt_test(data, qargs_B):
    state = DensityMatrix(data).to_statevector()
    return schmidt_decomposition(state, qargs_B)
