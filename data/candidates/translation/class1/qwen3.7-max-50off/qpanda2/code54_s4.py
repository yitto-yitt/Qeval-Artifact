# EVAL_META: task_id=54, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def and_gate(a, b):
    qmachine = init_quantum_machine(QMachineType.CPU)
    qa = qmachine.qAlloc(3)
    qb = qmachine.qAlloc(3)
    qanc = qmachine.qAlloc(3)
    ca = qmachine.cAlloc(3)
    
    prog = QProg()
    circ = QCircuit()
    
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    for i in range(3):
        if a_bin[2-i] == '1':
            circ << X(qa[i])
        if b_bin[2-i] == '1':
            circ << X(qb[i])
            
    for i in range(3):
        circ << Toffoli(qa[i], qb[i], qanc[i])
        
    for i in range(3):
        circ << Measure(qanc[i], ca[i])
        
    prog.insert(circ)
    
    result = qmachine.run_with_configuration(prog, ca, 1024)
    
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
