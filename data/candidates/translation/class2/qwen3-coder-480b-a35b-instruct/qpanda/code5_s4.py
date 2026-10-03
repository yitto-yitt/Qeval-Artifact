# EVAL_META: task_id=5, framework=qpanda, class=2
from pyqpanda3.core import *
import numpy as np

def create_state_prep():
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(2)
    
    # Create the state vector for |01> = [0, 1, 0, 0]
    state_vector = [0, 1, 0, 0]
    
    prog = QProg()
    prog.insert(prepare_state(qubits, state_vector))
    
    return prog
