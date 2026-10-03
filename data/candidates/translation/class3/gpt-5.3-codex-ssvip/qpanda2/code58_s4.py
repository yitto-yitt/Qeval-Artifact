# EVAL_META: task_id=58, framework=qpanda2, class=3
import pyqpanda as pq
from math import pi

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_ch_gate():
    prog = pq.QProg()
    prog.insert(pq.RY(q[1], pi / 4))
    prog.insert(pq.CNOT(q[0], q[1]))
    prog.insert(pq.RY(q[1], -pi / 4))
    return prog

machine.finalize()
