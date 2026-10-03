# EVAL_META: task_id=117, framework=qpanda, class=3
import pyqpanda3.core as pq
import numpy as np

def decompose_unitary(unitary):
    # Create a quantum program
    prog = pq.QProg()
    
    # Get quantum registers
    qubits = pq.qAlloc_many(2)
    
    # In pyQPanda3, we need to decompose the 4x4 unitary using CNOT gates
    # We'll use the built-in decomposition functionality
    circuit = pq.decompose_2q_unitary(unitary, pq.CNOT, qubits[0], qubits[1])
    
    return circuit
