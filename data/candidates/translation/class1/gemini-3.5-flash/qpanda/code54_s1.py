# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import *

def and_gate(a, b):
    machine = CPUQVM()
    machine.init_qvm()
    
    q = machine.qAlloc_many(9)
    c = machine.cAlloc_many(3)
    
    qr_a = q[0:3]
    qr_b = q[3:6]
    ancillary = q[6:9]
    
    prog = QProg()
    
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    for i in range(3):
        if a_str[2-i] == '1':
            prog << X(qr_a[i])
        if b_str[2-i] == '1':
            prog << X(qr_b[i])
            
    for i in range(3):
        prog << Toffoli(qr_a[i], qr_b[i], ancillary[i])
        
    for i in range(3):
        prog << Measure(ancillary[i], c[i])
        
    shots = 1000
    result = machine.run_with_configuration(prog, c, shots)
    
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
