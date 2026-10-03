# EVAL_META: task_id=90, framework=qpanda, class=3
import pyqpanda3 as pq
from pyqpanda3.core import *

def create_custom_controlled():
    # Create a quantum program
    prog = pq.QProg()
    
    # Create 4 qubits
    qubits = pq.qAlloc_many(4)
    
    # Create a sub-program for the custom gate (X on qubit 0, H on qubit 1)
    custom_prog = pq.QProg()
    custom_prog << pq.X(qubits[0]) << pq.H(qubits[1])
    
    # To implement a controlled version, we need to use controlled gates directly
    # For a 2-controlled operation, we apply the custom operations conditionally
    
    # Since pyQPanda doesn't have a direct "control" method like Qiskit,
    # we manually implement the controlled behavior using CNOT and other controlled gates
    # We'll build the equivalent controlled operation
    
    # The custom gate does X on qubit 1 and H on qubit 2 (in the context of the full circuit)
    # Controls are on qubits 0 and 3, targets are on qubits 1 and 2
    
    # Build the controlled version manually
    controlled_prog = pq.QProg()
    
    # This is equivalent to applying the custom gate (X on target[0], H on target[1])
    # only when both control qubits (0 and 3) are in |1> state
    controlled_prog << pq.CCX(qubits[0], qubits[3], qubits[1])  # Controlled-X on qubit 1
    controlled_prog << pq.create_CnGate(pq.H, [qubits[0], qubits[3]], qubits[2])  # Controlled-H on qubit 2
    
    prog << controlled_prog
    
    return prog
