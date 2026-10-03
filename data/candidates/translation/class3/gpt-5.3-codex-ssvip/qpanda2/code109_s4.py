# EVAL_META: task_id=109, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def circuit():
    prog = pq.QProg()
    theta = pq.var(0.0)
    prog << pq.H(q[0]) << pq.RZ(q[0], theta)
    return prog

machine.finalize()
