# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def circuit():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(1)
    
    prog = QProg()
    prog << H(qubits[0])
    
    # In pyQPanda3, we create a parameterized program
    theta = create_parameter("th")
    prog << RZ(qubits[0], theta)
    
    return prog, qubits, qvm
