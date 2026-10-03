# EVAL_META: task_id=58, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def create_ch_gate():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    prog = QProg()
    prog << RY(qubits[1], np.pi/4) \
         << CNOT(qubits[0], qubits[1]) \
         << RY(qubits[1], -np.pi/4)
    return prog
