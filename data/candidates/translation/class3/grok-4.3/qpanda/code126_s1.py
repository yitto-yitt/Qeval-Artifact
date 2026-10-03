# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, H

def calculate_phase_difference_fidelity():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(1)
    prog = QProg()
    prog << H(qubits[0])
    op_a = qvm.get_unitary(prog)
    op_b = np.exp(1j * 0.5) * op_a
    d = op_a.shape[0]
    fidelity = np.abs(np.trace(op_a.conj().T @ op_b)) ** 2 / d ** 2
    qvm.finalize()
    return float(fidelity)
