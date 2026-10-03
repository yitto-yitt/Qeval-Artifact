# EVAL_META: task_id=145, framework=qpanda, class=3
import pyqpanda3 as pq
from pyqpanda3.core import *
from pyqpanda3.extensions import *

def qft_inverse(n):
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(n)
    
    # Create the inverse QFT circuit manually since there's no direct inverse QFT in pyqpanda3
    circuit = pq.QCircuit()
    
    # Apply inverse QFT: reverse the order of operations in standard QFT
    for i in range(n):
        # Apply Hadamard to the last qubit in the sequence
        circuit.insert(pq.H(qubits[n-1-i]))
        
        # Apply controlled rotations
        for j in range(i):
            # Apply controlled phase gate with angle -pi/2^(i-j)
            angle = -pq.PI / (2 ** (i - j))
            circuit.insert(pq.CR(qubits[n-1-j], qubits[n-1-i], angle))
    
    # Reverse the order of qubits at the end (swap operations)
    for i in range(n // 2):
        circuit.insert(pq.SWAP(qubits[i], qubits[n-1-i]))
    
    return circuit
