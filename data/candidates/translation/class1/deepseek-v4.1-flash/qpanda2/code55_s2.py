# EVAL_META: task_id=55, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def or_gate(a, b):
    init_quantum_machine(QMachineType.CPU)
    qa = qAlloc_many(3)
    qb = qAlloc_many(3)
    anc = qAlloc_many(3)
    c = cAlloc_many(3)
    prog = QProg()
    
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    for i in range(3):
        if a_bin[2 - i] == '0':
            prog << X(qa[i])
        if b_bin[2 - i] == '0':
            prog << X(qb[i])
            
    for i in range(3):
        prog << Toffoli(qa[i], qb[i], anc[i])
        
    for i in range(3):
        prog << X(anc[i])
        
    prog << measure(anc[2], c[0])
    prog << measure(anc[1], c[1])
    prog << measure(anc[0], c[2])
    
    shots = 1000
    result = run_with_configuration(prog, shots)
    
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
