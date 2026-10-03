# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def simons_algorithm(s):
    n = len(s)
    qr = QuantumRegister(2 * n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)
    
    # Apply Hadamard gates to the first n qubits
    for i in range(n):
        qc.h(qr[i])
        
    # Oracle for Simon's algorithm
    # We construct a function f such that f(x) = f(x ^ s)
    # A simple and correct way is to only copy x_i to y_i when s_i == '0'
    # When s_i == '1', y_i remains 0, ensuring the periodicity matches s
    s_rev = s[::-1]
    for i in range(n):
        if s_rev[i] == '0':
            qc.cx(qr[i], qr[i + n])
            
    # Apply Hadamard gates to the first n qubits
    for i in range(n):
        qc.h(qr[i])
        
    # Measure the first n qubits into the classical register 'c'
    for i in range(n):
        qc.measure(qr[i], cr[i])
        
    return qc
