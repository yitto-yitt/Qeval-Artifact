# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda3.core import *

def not_gate(a):
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAllocMany(8)
    cbits = machine.cAllocMany(8)
    
    prog = QProg()
    a_str = format(a, "08b")
    for i in range(8):
        if a_str[7-i] == "0":
            prog << X(qubits[i])
            
    for i in range(8):
        prog << Measure(qubits[i], cbits[i])
        
    result = machine.run_with_configuration(prog, cbits, 1024)
    
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
