# EVAL_META: task_id=13, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
import atexit

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

atexit.register(machine.finalize)

def custom_rotation_gate():
    prog = QProg()
    prog << U3(qubits[0], np.pi / 2, np.pi / 2, np.pi / 2)
    return prog
