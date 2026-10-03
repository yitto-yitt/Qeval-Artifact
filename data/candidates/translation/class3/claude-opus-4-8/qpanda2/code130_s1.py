# EVAL_META: task_id=130, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)

def inv_circuit(n):
    prog = QProg()
    qv = qubits[:n]
    
    for i in range(2):
        prog << H(qv[i+1])
    
    for i in range(2):
        prog << CNOT(qv[i+1], qv[i+2+1])
    
    inverse_prog = QProg()
    for i in range(1, -1, -1):
        inverse_prog << CNOT(qv[i+1], qv[i+2+1])
    
    for i in range(1, -1, -1):
        inverse_prog << H(qv[i+1])
    
    return inverse_prog

machine.finalize()
