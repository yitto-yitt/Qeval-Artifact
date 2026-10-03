# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def calculate_phase_difference_fidelity():
    prog = QProg()
    prog << H(qubits[0])
    op_a = np.array(get_matrix(prog))
    op_b = np.exp(1j * 0.5) * op_a
    d = op_a.shape[0]
    trace = np.trace(np.conj(op_a.T) @ op_b)
    fidelity = np.abs(trace)**2 / (d**2)
    return fidelity

if __name__ == "__main__":
    print(calculate_phase_difference_fidelity())
    machine.finalize()
