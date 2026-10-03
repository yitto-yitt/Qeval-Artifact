# EVAL_META: task_id=106, framework=qpanda, class=3
import pyqpanda3.core as pq


def compose_cnot_dihedral():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)

    prog = pq.QProg()
    # First circuit: cx(0, 1), t(0)
    prog << pq.CNOT(q[0], q[1]) << pq.T(q[0])
    # Second circuit: cx(0, 1), t(0), x(1)
    prog << pq.CNOT(q[0], q[1]) << pq.T(q[0]) << pq.X(q[1])

    return prog
