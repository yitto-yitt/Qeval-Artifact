# EVAL_META: task_id=5, framework=qpanda, class=2
import pyqpanda3.core as pq


def create_state_prep():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.X(q[0])
    prog._machine = machine
    prog._q = q
    return prog
