# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, Qubit, X, Measure

def not_gate(a):
    a_bin = format(a, '08b')
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(8)
    c = qvm.cAlloc_many(8)
    prog = QProg()
    
    for i in range(8):
        if a_bin[7 - i] == '0':
            prog << X(q[i])
    
    for i in range(8):
        prog << Measure(q[i], c[i])
    
    result = qvm.run_with_configuration(prog, c, shots=1024)
    total = sum(result.values())
    return {k: v / total for k, v in result.items()}
