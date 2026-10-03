# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def simons_algorithm(s):
    n = len(s)
    qr = QuantumRegister(2 * n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)
    
    for i in range(n):
        qc.h(i)
        
    c = s.find('1')
    if c != -1:
        for i in range(n):
            if s[i] == '1':
                qc.cx(c, n + i)
                
    for i in range(n):
        qc.cx(i, n + i)
        
    for i in range(n):
        qc.h(i)
        
    for i in range(n):
        qc.measure(i, cr[i])
        
    return qc
