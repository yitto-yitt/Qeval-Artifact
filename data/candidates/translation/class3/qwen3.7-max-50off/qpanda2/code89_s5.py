# EVAL_META: task_id=89, framework=qpanda2, class=3
import pyqpanda as pq
import math

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def create_controlled_hgate():
    prog = pq.QProg()
    prog << pq.RY(q[2], -math.pi / 8)
    prog << pq.H(q[2])
    prog << pq.Toffoli(q[0], q[1], q[2])
    prog << pq.H(q[2])
    prog << pq.RY(q[2], math.pi / 8)
    return prog

machine.finalize()
