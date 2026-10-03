# EVAL_META: task_id=6, framework=qpanda, class=2
from pyqpanda3.core import *
import numpy as np

def create_state_prep(num_qubits):
    machine = CPUQVM()
    machine.init_qvm()
    qv = machine.qAlloc_many(num_qubits)
    
    # Create a quantum program that prepares the |1> state
    prog = QProg()
    
    # Apply X gate to the first qubit to prepare |1> state
    prog.insert(X(qv[0]))
    
    # For multi-qubit case, we need to tensor product with |0> states for other qubits
    # But since we want to prepare state |1> (which means the first qubit is |1> and others are |0>)
    # We just apply X to first qubit and leave others in |0>
    
    machine.finalize()
    return prog
