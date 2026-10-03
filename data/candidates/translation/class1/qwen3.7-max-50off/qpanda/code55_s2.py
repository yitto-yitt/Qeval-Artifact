# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import QuantumMachine, QProg, X, CCX, Measure

def or_gate(a, b):
    qm = QuantumMachine()
    qr_a = qm.qAlloc_many(3)
    qr_b = qm.qAlloc_many(3)
    ancillary = qm.qAlloc_many(3)
    c = qm.cAlloc_many(3)
    
    prog = QProg()
    
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    for i in range(3):
        if a_bin[2-i] == '0':
            prog << X(qr_a[i])
        if b_bin[2-i] == '0':
            prog << X(qr_b[i])
            
    for i in range(3):
        prog << CCX(qr_a[i], qr_b[i], ancillary[i])
        
    for i in range(3):
        prog << X(ancillary[i])
        
    for i in range(3):
        prog << Measure(ancillary[i], c[i])
        
    result = qm.run_with_configuration(prog, c, 1000)
    
    total = sum(result.values())
    return {k: v / total for k, v in result.items()}
