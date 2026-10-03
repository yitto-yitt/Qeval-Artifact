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
    
    # Create a QProg
    prog = QProg()
    
    # Add the unitary operation (equivalent to XX operator)
    prog.insert(CX(qubits[0], qubits[1]))
    prog.insert(X(qubits[0]))
    prog.insert(X(qubits[1]))
    
    # Since pyQPanda doesn't have direct operator append like Qiskit,
    # we manually construct the equivalent circuit for the given unitary
    # The given matrix is actually a SWAP gate followed by X on both qubits
    final_prog = QProg()
    final_prog.insert(SWAP(qubits[0], qubits[1]))
    final_prog.insert(X(qubits[0]))
    final_prog.insert(X(qubits[1]))
    
    # Perform optimization - in pyqpanda this would be done through optimization passes
    optimized_prog = transform_to_qrunes(final_prog, machine)
    
    destroy_quantum_machine(machine)
    
    return final_prog
