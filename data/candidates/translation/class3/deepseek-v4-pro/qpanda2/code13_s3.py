# EVAL_META: task_id=13, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)

def custom_rotation_gate():
    circuit = QProg()
    circuit << U3(q[0], np.pi / 2, np.pi / 2, np.pi / 2)
    return circuit

machine.finalize()
