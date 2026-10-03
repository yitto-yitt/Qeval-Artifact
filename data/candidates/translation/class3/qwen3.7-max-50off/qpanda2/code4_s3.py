# EVAL_META: task_id=4, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init()
q = machine.qAlloc_many(2)

def create_unitary_from_matrix():
    prog = pq.QProg()
    prog << pq.CNOT(q[1], q[0]) << pq.X(q[1])
    return prog

machine.finalize()
