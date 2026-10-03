# EVAL_META: task_id=13, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, U
import numpy as np

def custom_rotation_gate():
    qvm = CPUQVM()
    qvm.initQVM()
    qubits = qvm.qAllocMany(1)
    prog = QProg()
    prog << U(qubits[0], np.pi / 2, np.pi / 2, np.pi / 2)
    return prog
