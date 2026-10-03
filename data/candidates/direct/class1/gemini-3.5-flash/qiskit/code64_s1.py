# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def simons_algorithm(s):
    n = len(s)
    qr = QuantumRegister(2 * n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)
    
    # Apply Hadamard gates to the first n qubits
    for i in range(n):
        qc.h(i)
        
    # Oracle: f(x) = f(x ^ s)
    # 1. Copy the first n qubits to the second n qubits
    for i in range(n):
        qc.cx(i, i + n)
        
    # 2. If s is not all '0's, find the first '1' and use it to condition the XOR
    if '1' in s:
        c = s.find('1')
        for j in range(n):
            if s[j] == '1':
                qc.cx(c, j + n)
                
    # Apply Hadamard gates to the first n qubits
    for i in range(n):
        qc.h(i)
        
    # Measure the first n qubits
    for i in range(n):
        qc.measure(i, i)
        
    return qc
