# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, Measure

def not_gate(a):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(8)
    c = machine.cAlloc_many(8)
    prog = QProg()
    
    a_str = format(a, "08b")
    for i in range(8):
        if a_str[7-i] == "0":
            prog << X(q[i])
            
    for i in range(8):
        prog << Measure(q[i], c[i])
        
    result = machine.run_with_configuration(prog, c[::-1], 1000)
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
