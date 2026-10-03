# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def simons_algorithm(s):
    n = len(s)
    q = QuantumRegister(2 * n, 'q')
    c = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(q, c)
    
    # Apply Hadamard to the first register
    qc.h(range(n))
    
    # Build the oracle for the given s
    # Copy first register to second register
    for i in range(n):
        qc.cx(i, i + n)
    
    # Find a pivot qubit where s has a '1'
    if '1' in s:
        k = s.index('1')
        for i in range(n):
            if s[i] == '1':
                qc.cx(k, i + n)
    
    # Apply Hadamard to the first register again
    qc.h(range(n))
    
    # Measure the first register into the classical register 'c'
    qc.measure(range(n), range(n))
    
    return qc
