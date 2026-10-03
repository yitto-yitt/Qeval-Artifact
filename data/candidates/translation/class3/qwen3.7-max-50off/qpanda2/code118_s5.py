# EVAL_META: task_id=118, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init()
q = machine.qAlloc_many(4)

def create_c3sx_circuit():
    prog = pq.QProg()
    prog << pq.RX(np.pi/2, q[3])
    return prog

machine.finalize()
