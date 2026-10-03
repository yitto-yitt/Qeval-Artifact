# EVAL_META: task_id=145, framework=qpanda, class=3
from pyqpanda3.core import *
import math

_machines = []

def qft_inverse(n):
    machine = CPUQVM()
    machine.init_qvm()
    _machines.append(machine)
    qubits = machine.qAlloc_many(n)
    
    circuit = QCircuit()
    for i in range(n):
        circuit << H(qubits[i])
        for j in range(i + 1, n):
            theta = 2 * math.pi / (2 ** (j - i + 1))
            circuit << CPHASE(qubits[j], qubits[i], theta)
            
    for i in range(n // 2):
        circuit << SWAP(qubits[i], qubits[n - 1 - i])
        
    return circuit.dagger()
