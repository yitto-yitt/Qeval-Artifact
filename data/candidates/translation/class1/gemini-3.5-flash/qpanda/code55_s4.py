# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, TOFFOLI, QVec

def or_gate(a, b):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(9)
    prog = QProg()
    
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    for i in range(3):
        if a_str[2-i] == '0':
            prog << X(q[i])
        if b_str[2-i] == '0':
            prog << X(q[3+i])
            
    for i in range(3):
        prog << TOFFOLI(q[i], q[3+i], q[6+i])
        
    for i in range(3):
        prog << X(q[6+i])
        
    qubits_to_measure = QVec()
    qubits_to_measure.append(q[8])
    qubits_to_measure.append(q[7])
    qubits_to_measure.append(q[6])
    
    result = machine.prob_run_dict(prog, qubits_to_measure)
    return {k: v for k, v in result.items() if v > 0}
