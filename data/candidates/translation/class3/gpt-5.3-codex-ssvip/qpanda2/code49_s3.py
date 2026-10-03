# EVAL_META: task_id=49, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def simple_elitzur_vaidman():
    prog = pq.QProg()
    prog.insert(pq.H(q[0]))
    prog.insert(pq.CNOT(q[0], q[1]))
    prog.insert(pq.H(q[0]))
    return prog

machine.finalize()
