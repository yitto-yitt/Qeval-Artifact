# EVAL_META: task_id=5, framework=qpanda2, class=2
import pyqpanda as pq


def create_state_prep():
    pq.init()
    q = pq.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.X(q[0])
    return prog
