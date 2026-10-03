# EVAL_META: task_id=78, framework=qpanda, class=3
from pyqpanda3.core import *
import math

def qft_no_swaps(num_qubits):
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(num_qubits)
    circuit = QCircuit()
    
    for i in range(num_qubits):
        for j in range(i):
            angle = -math.pi / (2 ** (i - j))
            circuit << CR(qubits[j], qubits[i], angle)
        circuit << H(qubits[i])
        
    return circuit
