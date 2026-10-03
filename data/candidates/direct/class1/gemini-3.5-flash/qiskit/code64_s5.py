# EVAL_META: task_id=64, framework=qiskit, class=1

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def simons_algorithm(s):
    n = len(s)
    qr = QuantumRegister(2 * n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)
    
    # Apply Hadamard gates to the first register
    for i in range(n):
        qc.h(qr[i])
        
    # Apply the oracle
    # 1. Copy the first register to the second register
    for i in range(n):
        qc.cx(qr[i], qr[n + i])
        
    # 2. XOR with s based on the first '1' bit
    k = s.find('1')
    if k != -1:
        for i in range(n):
            if s[i] == '1':
                qc.cx(qr[k], qr[n + i])
                
    # Apply Hadamard gates to the first register
    for i in range(n):
        qc.h(qr[i])
        
    # Measure the first register
    for i in range(n):
        qc.measure(qr[i], cr[i])
        
    return qc
