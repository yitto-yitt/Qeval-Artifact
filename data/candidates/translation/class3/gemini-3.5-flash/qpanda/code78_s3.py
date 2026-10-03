# EVAL_META: task_id=78, framework=qpanda, class=3
import math
from pyqpanda3.core import *

def qft_no_swaps(num_qubits):
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qalloc_many(num_qubits)
    
    prog = QProg()
    for i in range(num_qubits):
        prog << H(qubits[i])
        for j in range(i + 1, num_qubits):
            angle = -math.pi / (2 ** (j - i))
            prog << CU1(qubits[j], qubits[i], angle)
            
    return prog
