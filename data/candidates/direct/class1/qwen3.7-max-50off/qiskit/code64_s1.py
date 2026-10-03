# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def simons_algorithm(s):
    n = len(s)
    qr_x = QuantumRegister(n, 'x')
    qr_y = QuantumRegister(n, 'y')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr_x, qr_y, cr)
    
    # Apply Hadamard to all input qubits
    qc.h(qr_x)
    
    # Apply Oracle for Simon's Algorithm
    if '1' not in s:
        for i in range(n):
            qc.cx(qr_x[i], qr_y[i])
    else:
        k = s.find('1')
        for i in range(n):
            qc.cx(qr_x[i], qr_y[i])
        for i in range(n):
            if s[i] == '1':
                qc.cx(qr_x[k], qr_y[i])
                
    # Apply Hadamard to all input qubits
    qc.h(qr_x)
    
    # Measure input qubits into classical register 'c'
    qc.measure(qr_x, cr)
    
    return qc
