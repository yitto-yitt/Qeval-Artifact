# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister


def simons_algorithm(s):
    n = len(s)
    
    # Create quantum and classical registers
    qr = QuantumRegister(2 * n)
    cr = ClassicalRegister(n)
    qc = QuantumCircuit(qr, cr)
    
    # Apply Hadamard gates to the first n qubits
    for i in range(n):
        qc.h(i)
    
    # Implement the oracle function that computes f(x) = x XOR s if x != 0^n, else f(x) = 0^n
    # This implementation creates the desired behavior where f(x) XOR s = s
    # We'll create a mapping that effectively encodes the Simon's problem structure
    for i in range(n):
        if s[i] == '1':
            # For each position where s has a 1, we need to implement the appropriate transformation
            # Connect the first register to the second register using CNOT gates
            qc.cx(i, n + i)
    
    # Apply Hadamard gates again to the first n qubits
    for i in range(n):
        qc.h(i)
    
    # Measure the first n qubits
    for i in range(n):
        qc.measure(i, i)
        
    return qc
