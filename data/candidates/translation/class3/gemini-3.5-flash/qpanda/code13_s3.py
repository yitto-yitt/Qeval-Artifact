# EVAL_META: task_id=13, framework=qpanda, class=3
import pyqpanda3.core as pq
import numpy as np

machine = None

def custom_rotation_gate():
    global machine
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    prog = pq.QProg()
    prog << pq.U3(q[0], np.pi / 2, np.pi / 2, np.pi / 2)
    return prog
