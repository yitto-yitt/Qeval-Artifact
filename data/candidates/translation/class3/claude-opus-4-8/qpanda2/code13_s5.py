# EVAL_META: task_id=13, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def custom_rotation_gate():
    prog = QProg()
    prog << U4(np.pi / 2, np.pi / 2, np.pi / 2, np.pi / 2, qubits[0])
    return prog

machine.finalize()
