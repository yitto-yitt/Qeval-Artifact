# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
import atexit
from pyqpanda import *

qvm = CPUQVM()
qvm.init_qvm()
qubits = qvm.qAlloc_many(1)
atexit.register(qvm.finalize)

def calculate_phase_difference_fidelity():
    # Get first column of H matrix: H|0>
    prog0 = QProg()
    prog0 << H(qubits[0])
    res0 = qvm.run(prog0, qubits)
    state0 = np.zeros(2, dtype=complex)
    for k, v in res0.items():
        state0[k] = v

    # Get second column of H matrix: H|1> = H X|0>
    prog1 = QProg()
    prog1 << X(qubits[0]) << H(qubits[0])
    res1 = qvm.run(prog1, qubits)
    state1 = np.zeros(2, dtype=complex)
    for k, v in res1.items():
        state1[k] = v

    op_a = np.column_stack((state0, state1))
    op_b = np.exp(1j * 0.5) * op_a

    fidelity = np.abs(np.trace(op_a.conj().T @ op_b))**2 / (op_a.shape[0]**2)
    return fidelity.real
