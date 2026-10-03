# EVAL_META: task_id=10, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import *
import numpy as np

def create_operator():
    # Define the unitary matrix
    matrix = np.array([[0, 0, 0, 1], 
                       [0, 0, 1, 0], 
                       [0, 1, 0, 0], 
                       [1, 0, 0, 0]], dtype=complex)
    
    # Create a quantum machine
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    
    # Create a quantum program
    prog = QProg()
    
    # Add the unitary operation using the matrix
    prog.insert(CR(qubits[0], qubits[1], matrix))
    
    # Since pyQPanda3 doesn't have direct equivalent to Qiskit's transpilation,
    # we return the program as is after optimization (if available)
    # The CR gate already implements the desired unitary
    
    destroy_quantum_machine(machine)
    return prog
