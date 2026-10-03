# EVAL_META: task_id=139, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import Statevector, DensityMatrix, schmidt_decomposition


def schmidt_test(data, qargs_B):
    try:
        arr = np.asarray(data.data if hasattr(data, "data") else data)
        if arr.ndim == 1 or (arr.ndim == 2 and 1 in arr.shape):
            return schmidt_decomposition(Statevector(np.ravel(arr)), qargs_B)
    except Exception:
        pass

    try:
        return schmidt_decomposition(data, qargs_B)
    except Exception:
        dm = DensityMatrix(data)
        rho = np.asarray(dm.data, dtype=complex)
        dims = dm.dims()

        tr = np.trace(rho)
        if abs(tr) > 0:
            rho = rho / tr

        diag = np.real_if_close(np.diag(rho)).real
        k = int(np.argmax(diag))
        if diag[k] > 1e-12:
            vec = rho[:, k] / np.sqrt(diag[k])
        else:
            vals, vecs = np.linalg.eigh(rho)
            vec = vecs[:, int(np.argmax(vals))]

        idx = int(np.argmax(np.abs(vec)))
        if abs(vec[idx]) > 1e-12:
            vec = vec * np.exp(-1j * np.angle(vec[idx]))

        return schmidt_decomposition(Statevector(vec, dims=dims), qargs_B)
