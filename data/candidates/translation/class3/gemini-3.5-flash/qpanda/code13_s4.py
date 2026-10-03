# EVAL_META: task_id=13, framework=qpanda, class=3
import pyqpanda3.core as pq
import numpy as np

def custom_rotation_gate():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc()
    prog = pq.QProg()
    prog << pq.U3(q, np.pi / 2, np.pi / 2, np.pi / 2)
    return prog
