# EVAL_META: task_id=59, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_cz_gate():
    prog = pq.QProg()
    prog.insert(pq.H(q[1]))
    prog.insert(pq.CNOT(q[0], q[1]))
    prog.insert(pq.H(q[1]))
    return prog

machine.finalize()
