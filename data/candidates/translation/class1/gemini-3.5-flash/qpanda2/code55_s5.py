# EVAL_META: task_id=55, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def or_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    
    qubits = qvm.qAlloc_many(9)
    cbits = qvm.cAlloc_many(3)
    
    prog = QProg()
    
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    for i in range(3):
        if a_str[2-i] == '0':
            prog << X(qubits[i])
        if b_str[2-i] == '0':
            prog << X(qubits[3+i])
            
    for i in range(3):
        prog << X(qubits[6+i]).control([qubits[i], qubits[3+i]])
        
    for i in range(3):
        prog << X(qubits[6+i])
        
    for i in range(3):
        prog << Measure(qubits[6+i], cbits[i])
        
    shots = 1000
    result = qvm.run_with_configuration(prog, cbits, shots)
    
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
