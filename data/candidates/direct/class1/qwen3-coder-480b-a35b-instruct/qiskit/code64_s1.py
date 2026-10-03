# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister

def simons_algorithm(s):
    n = len(s)
    qc = QuantumCircuit(2 * n, n)
    
    # Apply Hadamard gates to the first n qubits
    for i in range(n):
        qc.h(i)
    
    # Add classical register named 'c'
    c_reg = ClassicalRegister(n, 'c')
    qc.add_register(c_reg)
    
    # Apply the oracle
    for i in range(n):
        if s[i] == '1':
            qc.cx(i, n + i)
    
    # Apply CNOT gates based on the pattern of s
    for i in range(n):
        for j in range(n):
            if s[j] == '1':
                qc.cx(i, n + j)
    
    # Apply Hadamard gates to the first n qubits again
    for i in range(n):
        qc.h(i)
    
    # Measure the first n qubits
    for i in range(n):
        qc.measure(i, i)
    
    return qc
