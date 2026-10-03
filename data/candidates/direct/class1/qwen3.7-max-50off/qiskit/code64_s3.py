# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def simons_algorithm(s):
    n = len(s)
    qr = QuantumRegister(n, 'q')
    out = QuantumRegister(n, 'out')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, out, cr)
    
    for i in range(n):
        qc.h(qr[i])
        
    k = -1
    for i in range(n):
        if str(s[i]) == '1':
            k = i
            break
            
    for i in range(n):
        qc.cx(qr[i], out[i])
        
    if k != -1:
        for i in range(n):
            if str(s[i]) == '1':
                qc.cx(qr[k], out[i])
                
    for i in range(n):
        qc.h(qr[i])
        
    qc.measure(qr, cr)
    
    return qc
