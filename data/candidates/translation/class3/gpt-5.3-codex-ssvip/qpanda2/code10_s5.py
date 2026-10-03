# EVAL_META: task_id=10, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)
c = machine.cAlloc_many(2)

def create_operator():
    prog = pq.QProg()
    prog.insert(pq.X(q[0]))
    prog.insert(pq.X(q[1]))
    return prog

machine.finalize()
