# EVAL_META: task_id=13, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def custom_rotation_gate():
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(1)
    prog = QProg()
    prog << U3(qubits[0], np.pi / 2, np.pi / 2, np.pi / 2)
    return prog
