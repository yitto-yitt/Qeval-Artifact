# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import DensityMatrix, Statevector

def schmidt_test(data, qargs_B):
    if isinstance(qargs_B, int):
        qargs_B = [qargs_B]
    if hasattr(data, 'schmidt_decomposition'):
        return data.schmidt_decomposition(qargs_B)
    if isinstance(data, DensityMatrix):
        return data.to_statevector().schmidt_decomposition(qargs_B)
    arr = np.asarray(data)
    if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        return DensityMatrix(data).to_statevector().schmidt_decomposition(qargs_B)
    return Statevector(data).schmidt_decomposition(qargs_B)
