# EVAL_META: task_id=12, framework=qpanda2, class=3
import pyqpanda as pq
machine = pq.CPUQVM()
machine.initQVM()
q = machine.qAlloc_many(2)
def get_unitary():
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    return pq.get_unitary_matrix(prog)
machine.finalize()
