# EVAL_META: task_id=54, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def and_gate(a, b):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(9)
    c = machine.cAlloc_many(3)
    prog = QProg()
    
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    for i in range(3):
        if a_bin[2-i] == '1':
            prog << X(q[i])
        if b_bin[2-i] == '1':
            prog << X(q[3+i])
    
    for i in range(3):
        prog << Toffoli(q[i], q[3+i], q[6+i])
    
    for i in range(3):
        prog << Measure(q[8-i], c[i])
    
    shots = 1024
    result = machine.run_with_configuration(prog, c, shots)
    machine.finalize()
    
    total = shots
    return {key: value / total for key, value in result.items()}
