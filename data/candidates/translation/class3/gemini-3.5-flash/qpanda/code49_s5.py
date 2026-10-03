# EVAL_META: task_id=49, framework=qpanda, class=3
import pyqpanda3.core as pq

def simple_elitzur_vaidman():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.H(q[0])
    return prog
