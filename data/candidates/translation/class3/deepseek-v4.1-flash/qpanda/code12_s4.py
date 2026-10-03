# EVAL_META: task_id=12, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, X

def get_unitary():
    n = 2
    dim = 1 << n

    # Detect qubit ordering
    cal_qvm = CPUQVM()
    cal_qvm.init_qvm()
    q_cal = cal_qvm.qAlloc_many(n)
    prog_cal = QProg()
    prog_cal << X(q_cal[0])
    cal_qvm.run(prog_cal)
    state_cal = np.array(cal_qvm.get_qstate())
    idx = int(np.argmax(np.abs(state_cal)))

    if idx == 1:
        map_q_to_p = [0, 1]
    elif idx == 2:
        map_q_to_p = [1, 0]
    else:
        map_q_to_p = [0, 1]

    M = np.zeros((dim, dim), dtype=complex)

    for j in range(dim):
        qvm = CPUQVM()
        qvm.init_qvm()
        q = qvm.qAlloc_many(n)
        prog = QProg()

        if (j >> 0) & 1:
            prog << X(q[map_q_to_p[0]])
        if (j >> 1) & 1:
            prog << X(q[map_q_to_p[1]])

        prog << H(q[map_q_to_p[0]])
        prog << CNOT(q[map_q_to_p[0]], q[map_q_to_p[1]])

        qvm.run(prog)
        state = np.array(qvm.get_qstate())
        M[:, j] = state

    return M
