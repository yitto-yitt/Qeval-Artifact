# EVAL_META: task_id=139, framework=qiskit, class=2
from qiskit.quantum_info import DensityMatrix, Statevector, schmidt_decomposition
import numpy as np

def schmidt_test(data, qargs_B):
    if isinstance(data, DensityMatrix):
        data = data.to_statevector()
    elif isinstance(data, np.ndarray):
        if data.ndim == 2:
            data = DensityMatrix(data).to_statevector()
        else:
            data = Statevector(data)
    elif not isinstance(data, Statevector):
        data = Statevector(data)
    
    if isinstance(qargs_B, int):
        qargs_B = [qargs_B]
    qargs_B_set = set(qargs_B)
    num_qubits = data.num_qubits
    qargs_A = [q for q in range(num_qubits) if q not in qargs_B_set]
    return schmidt_decomposition(data, qargs_A)
