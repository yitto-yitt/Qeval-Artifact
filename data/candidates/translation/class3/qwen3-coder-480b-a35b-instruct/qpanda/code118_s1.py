# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda import *

def create_c3sx_circuit():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(4)
    cbits = qvm.cAlloc_many(4)
    
    prog = QProg()
    prog.insert(C3SX(qubits[0], qubits[1], qubits[2], qubits[3]))
    
    return prog
