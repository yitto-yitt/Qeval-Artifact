# EVAL_META: task_id=139, framework=qiskit, class=2
from qiskit.quantum_info import Statevector, DensityMatrix, schmidt_decomposition
import numpy as np

def schmidt_test(data, qargs_B):
    if isinstance(data, Statevector):
        state = data
    elif isinstance(data, DensityMatrix):
        try:
            state = data.to_statevector()
        except Exception:
            vals, vecs = np.linalg.eigh(data.data)
            idx = np.argmax(vals)
            state = Statevector(vecs[:, idx])
    else:
        arr = np.asarray(data)
        if arr.ndim == 2 and arr.shape[0] == arr.shape[1]:
            vals, vecs = np.linalg.eigh(arr)
            idx = np.argmax(vals)
            state = Statevector(vecs[:, idx])
        else:
            state = Statevector(arr.flatten())
    
    num_qubits = state.num_qubits
    if isinstance(qargs_B, int):
        qargs_B = [qargs_B]
    if qargs_B is None:
        qargs_B = list(range(num_qubits // 2, num_qubits))
    qargs_A = [q for q in range(num_qubits) if q not in set(qargs_B)]
    
    return schmidt_decomposition(state, qargs_A)
