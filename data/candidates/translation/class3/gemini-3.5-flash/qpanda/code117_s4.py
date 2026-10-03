# EVAL_META: task_id=117, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def decompose_unitary(unitary):
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    
    if hasattr(unitary, 'data'):
        unitary = unitary.data
    matrix = np.array(unitary).flatten().tolist()
    
    circuit = matrix_decompose(qubits, matrix)
    return circuit
