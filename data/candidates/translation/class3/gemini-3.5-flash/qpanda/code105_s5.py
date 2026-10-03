# EVAL_META: task_id=105, framework=qpanda, class=3
import pyqpanda3.core as pq


def initialize_cnot_dihedral():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.CNOT(q[0], q[1]) << pq.T(q[0])
    return prog
