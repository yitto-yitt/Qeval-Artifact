# EVAL_META: task_id=10, framework=qpanda, class=3
import pyqpanda3 as pq

def create_operator():
    q = pq.QVec(2)
    prog = pq.QProg()
    prog << pq.CX(q[0], q[1]) << pq.CX(q[1], q[0]) << pq.CX(q[0], q[1])
    return prog
