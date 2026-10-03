# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def simons_algorithm(s):
    n = len(s)
    qr = QuantumRegister(2 * n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)
    
    # Apply Hadamard gates to the input register
    for i in range(n):
        qc.h(qr[i])
        
    # Oracle: Copy input to output register
    for i in range(n):
        qc.cx(qr[i], qr[i + n])
        
    # Oracle: Apply XOR based on the period s
    s_rev = s[::-1]
    if '1' in s_rev:
        k = s_rev.index('1')
        for j in range(n):
            if s_rev[j] == '1':
                qc.cx(qr[k], qr[j + n])
                
    # Apply Hadamard gates to the input register again
    for i in range(n):
        qc.h(qr[i])
        
    # Measure the input register
    qc.measure(qr[:n], cr)
    
    return qc
