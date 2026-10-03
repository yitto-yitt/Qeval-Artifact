# EVAL_META: task_id=78, framework=qpanda, class=3
from pyqpanda3.core import *
from math import pi

def qft_no_swaps(num_qubits):
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(num_qubits)
    
    circuit = QCircuit()
    for i in range(num_qubits):
        circuit << H(qubits[i])
        for j in range(i + 1, num_qubits):
            angle = -pi / (2 ** (j - i))
            circuit << CR(qubits[i], qubits[j], angle)
            
    return circuit
