# EVAL_META: task_id=65, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def QFT(n):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n)
    
    circuit = QCircuit()
    
    def qft_rotations(circuit, q, n):
        if n == 0:
            return
        n -= 1
        circuit << H(q[n])
        for qubit in range(n):
            circuit << CU1(q[qubit], q[n], np.pi / (2**(n-qubit)))
        qft_rotations(circuit, q, n)
        
    def swap_registers(circuit, q, n):
        for qubit in range(n // 2):
            circuit << SWAP(q[qubit], q[n-qubit-1])
            
    qft_rotations(circuit, q, n)
    swap_registers(circuit, q, n)
    
    return circuit
