# EVAL_META: task_id=126, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def calculate_phase_difference_fidelity():
    # Extract unitary of Hadamard gate by simulating on |0> and |1>
    machine.run(QProg() << RESET(q[0]))
    machine.run(QProg() << H(q[0]))
    state0 = machine.get_qstate()

    machine.run(QProg() << RESET(q[0]) << X(q[0]) << H(q[0]))
    state1 = machine.get_qstate()

    U_H = np.array([[state0[0], state1[0]],
                    [state0[1], state1[1]]], dtype=complex)

    U_B = np.exp(1j * 0.5) * U_H

    d = U_H.shape[0]
    trace = np.trace(np.conj(U_H).T @ U_B)
    fidelity = np.abs(trace)**2 / (d**2)

    machine.finalize()
    return float(fidelity)
