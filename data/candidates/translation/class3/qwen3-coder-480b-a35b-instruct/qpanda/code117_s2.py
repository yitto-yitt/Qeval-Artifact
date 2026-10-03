# EVAL_META: task_id=117, framework=qpanda, class=3
import pyqpanda3.core as pq
import numpy as np

def decompose_unitary(unitary):
    # Create a quantum machine
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(2)
    
    # Convert the unitary matrix to a pyQPanda3 circuit using decomposition
    # PyQPanda3 doesn't have direct equivalent to Qiskit's TwoQubitBasisDecomposer
    # We need to use the built-in decomposition functionality
    
    # Create a quantum program
    prog = pq.QProg()
    
    # Since pyQPanda3 doesn't have exact equivalent, we'll use the U4 gate decomposition
    # which can represent any 2-qubit unitary operation
    prog.insert(pq.decompose_unitary_double_qubit(qubits[0], qubits[1], unitary))
    
    return prog
