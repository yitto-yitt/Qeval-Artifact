# EVAL_META: task_id=23, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def dj_constant_oracle():
    prog = pq.QProg()
    prog << pq.X(q[2])
    return prog

machine.finalize()
