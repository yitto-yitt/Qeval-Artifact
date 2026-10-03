# EVAL_META: task_id=2, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import *

def create_bell_statevector():
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    
    prog = QProg()
    prog.insert(single_gate_apply_to_all(gate_type.H, qubits))
    prog.insert(CNOT(qubits[0], qubits[1]))
    
    stv = machine.get_statevector(prog)
    machine.finalize()
    
    return np.array(stv)
