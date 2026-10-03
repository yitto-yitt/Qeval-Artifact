# EVAL_META: task_id=89, framework=qpanda, class=3
import pyqpanda3 as pq
from pyqpanda3.core import *

def create_controlled_hgate():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = machine.qAlloc_many(3)
    
    prog = pq.QProg()
    # Create a controlled-H gate with 2 control qubits
    # Using H gate controlled by qubits[0] and qubits[1], targeting qubits[2]
    prog << pq.TOFFOLI(qubits[0], qubits[1], qubits[2]) << pq.H(qubits[2]) << pq.TOFFOLI(qubits[0], qubits[1], qubits[2])
    
    # Alternative approach: manually construct the controlled-H using CNOT and single-qubit gates
    # We need to implement a doubly-controlled H gate
    prog.clear()
    # First, we'll use a multi-controlled approach by decomposing
    ctrl_h = pq.create_empty_circuit()
    ctrl_h << pq.H(qubits[2]).controlled([qubits[0], qubits[1]])
    
    prog << ctrl_h
    
    return prog
