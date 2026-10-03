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
    s_rev = s[::-1]
    first_one = -1
    for i in range(n):
        if s_rev[i] == '1':
            first_one = i
            break
            
    if first_one == -1:
        # 1-to-1 mapping if s is all '0's
        for i in range(n):
            qc.cx(qr[i], qr[n + i])
    else:
        for i in range(n):
            if s_rev[i] == '0':
                qc.cx(qr[i], qr[n + i])
            else:
                qc.cx(qr[i], qr[n + i])
                qc.cx(qr[first_one], qr[n + i])
                
    # Apply Hadamard gates to the first register again
    for i in range(n):
        qc.h(qr[i])
        
    # Measure the first register
    for i in range(n):
        qc.measure(qr[i], cr[i])
        
    return qc
