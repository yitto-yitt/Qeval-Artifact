# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import *
import numpy as np

def create_uniform_superposition(n):
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(n)
    cbits = machine.cAlloc_many(n)
    
    prog = QProg()
    for i in range(n):
        prog.insert(H(qubits[i]))
    
    machine.directly_run(prog)
    result = machine.get_qstate()
    
    machine.finalize()
    
    return np.array(result)
