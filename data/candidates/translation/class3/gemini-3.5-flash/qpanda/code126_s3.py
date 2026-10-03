# EVAL_META: task_id=126, framework=qpanda, class=3
import numpy as np
import pyqpanda3.core as pq


def calculate_phase_difference_fidelity():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)

    prog = pq.QProg()
    prog << pq.H(q[0])

    unitary_list = machine.get_unitary_of_prog(prog)

    U_flat = np.array(unitary_list)
    V_flat = np.exp(1j * 0.5) * U_flat

    fidelity = np.abs(np.vdot(U_flat, V_flat)) ** 2 / 4.0

    machine.finalize()
    return fidelity
