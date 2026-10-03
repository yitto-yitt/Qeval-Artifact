# EVAL_META: task_id=6, framework=qpanda, class=2
from pyqpanda3.core import *

def create_state_prep(num_qubits):
    qvm = CPUQVM()
    qvm.initQVM()
    qubits = qvm.qAllocMany(num_qubits)
    prog = QProg()
    prog << X(qubits[0])
    return prog
