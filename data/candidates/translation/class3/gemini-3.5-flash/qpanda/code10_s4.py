# EVAL_META: task_id=10, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_operator():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.X(q[0]) << pq.X(q[1])
    return prog
