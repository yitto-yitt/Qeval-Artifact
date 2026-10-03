# EVAL_META: task_id=139, framework=qiskit, class=2
from qiskit.quantum_info import DensityMatrix

def schmidt_test(data, qargs_B):
    return data.schmidt_decomposition(qargs_B)
