# EVAL_META: task_id=139, framework=qiskit, class=2
from qiskit.quantum_info import Statevector, DensityMatrix
import numpy as np

def _as_statevector(data):
    if isinstance(data, Statevector):
        return data
    if isinstance(data, DensityMatrix):
        if data.purity() < 1 - 1e-12:
            raise ValueError("Density matrix is not pure")
        return data.to_statevector()

    arr = np.asarray(data)
    if arr.ndim == 1 or (arr.ndim == 2 and arr.shape[1] == 1):
        return Statevector(arr.ravel())
    if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
        dm = DensityMatrix(arr)
        if dm.purity() < 1 - 1e-12:
            raise ValueError("Density matrix is not pure")
        return dm.to_statevector()

    raise ValueError("Input must be a statevector or density matrix")

def schmidt_test(data, qargs_B):
    if isinstance(qargs_B, int):
        qargs_B = [qargs_B]
    else:
        qargs_B = list(qargs_B)

    if isinstance(data, (Statevector, DensityMatrix)) and hasattr(data, "schmidt_decomposition"):
        return data.schmidt_decomposition(qargs_B)

    psi = _as_statevector(data)
    return psi.schmidt_decomposition(qargs_B)
