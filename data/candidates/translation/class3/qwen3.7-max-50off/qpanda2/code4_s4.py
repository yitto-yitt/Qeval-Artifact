# EVAL_META: task_id=4, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_unitary_from_matrix():
    prog = pq.QProg()
    prog << pq.SWAP(q[0], q[1])
    return prog

machine.finalize()
