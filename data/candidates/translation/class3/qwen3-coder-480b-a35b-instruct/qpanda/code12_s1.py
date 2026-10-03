# EVAL_META: task_id=12, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np


def get_unitary():
    machine = init(QMachineType.CPU)
    prog = QProg()
    
    # Create quantum circuit for |Φ+⟩ Bell state
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    
    prog.insert(H(q[0]))
    prog.insert(CNOT(q[0], q[1]))
    
    # Get unitary matrix
    unitary = get_unitary_matrix(prog, machine)
    
    # Clean up
    machine.finalize()
    
    return unitary
