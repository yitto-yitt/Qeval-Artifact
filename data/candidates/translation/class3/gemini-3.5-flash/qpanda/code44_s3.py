# EVAL_META: task_id=44, framework=qpanda, class=3
import pyqpanda3.core as pq

def tensor_circuits():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(3)
    prog = pq.QProg()
    prog << pq.X(q[0]) << pq.CRY(q[1], q[2], 0.2)
    return prog
