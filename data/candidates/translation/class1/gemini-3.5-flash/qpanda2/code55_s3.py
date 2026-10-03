# EVAL_META: task_id=55, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def or_gate(a, b):
    machine = CPUQVM()
    machine.init_qvm()
    
    q = machine.qAlloc_many(9)
    c = machine.cAlloc_many(3)
    
    qr_a = [q[0], q[1], q[2]]
    qr_b = [q[3], q[4], q[5]]
    ancillary = [q[6], q[7], q[8]]
    
    prog = QProg()
    
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    for i in range(3):
        if a_str[2-i] == '0':
            prog << X(qr_a[i])
        if b_str[2-i] == '0':
            prog << X(qr_b[i])
            
    for i in range(3):
        prog << X(ancillary[i]).control([qr_a[i], qr_b[i]])
        
    for i in range(3):
        prog << X(ancillary[i])
        
    for i in range(3):
        prog << Measure(ancillary[i], c[i])
        
    shots = 1000
    result = machine.run_with_configuration(prog, c, shots)
    
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
