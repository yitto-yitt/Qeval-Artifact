# EVAL_META: task_id=44, framework=qpanda, class=3
import pyqpanda3.core as pq

def tensor_circuits():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    prog = pq.QProg()
    prog << pq.RY(q[1], 0.2).control([q[0]])
    prog << pq.X(q[2])
    return prog
