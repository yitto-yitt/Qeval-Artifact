# EVAL_META: task_id=44, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def tensor_circuits():
    prog = pq.QProg()
    prog << pq.X(q[0])
    prog << pq.RY(q[2], 0.2).control([q[1]])
    return prog

machine.finalize()
