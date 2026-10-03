# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import DensityMatrix, Statevector

def schmidt_test(data, qargs_B):
    if isinstance(data, Statevector):
        return data.schmidt_decomposition(qargs_B)

    if isinstance(data, DensityMatrix):
        if hasattr(data, 'schmidt_decomposition'):
            return data.schmidt_decomposition(qargs_B)
        return data.to_statevector().schmidt_decomposition(qargs_B)

    arr = np.asarray(data)
    if arr.ndim == 1:
        return Statevector(data).schmidt_decomposition(qargs_B)

    dm = DensityMatrix(data)
    if hasattr(dm, 'schmidt_decomposition'):
        return dm.schmidt_decomposition(qargs_B)
    return dm.to_statevector().schmidt_decomposition(qargs_B)
