# EVAL_META: task_id=117, framework=qpanda, class=3
import pyqpanda3.core as pq
import numpy as np

def decompose_unitary(unitary):
    # Convert the 4x4 unitary matrix to a format compatible with pyQPanda3
    # Create a quantum program to decompose the unitary
    prog = pq.QProg()
    qubits = pq.qAlloc(2)
    
    # In pyQPanda3, we need to use the appropriate decomposition method
    # Since there isn't a direct equivalent to Qiskit's TwoQubitBasisDecomposer,
    # we'll use the built-in unitary decomposition functionality
    prog.insert(pq.unitary_decompose(qubits, unitary))
    
    return prog
