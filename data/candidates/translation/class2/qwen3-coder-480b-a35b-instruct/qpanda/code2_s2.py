# EVAL_META: task_id=2, framework=qpanda, class=2
import pyqpanda3.core as pq
from pyqpanda3.core import *
import numpy as np


def create_bell_statevector():
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(2)
    
    # Create Bell state |Φ+⟩ = (|00⟩ + |11⟩) / √2
    prog = pq.QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    
    # Get state vector
    state_vector = machine.get_state_vector(prog)
    
    # Clean up
    machine.qFree_all(qubits)
    
    return state_vector
