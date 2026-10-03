# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

def simons_algorithm(s):
    s_str = ''.join(str(x) for x in s)
    n = len(s_str)
    
    qr = QuantumRegister(2 * n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)
    
    # Apply Hadamard gates to the first n qubits
    for i in range(n):
        qc.h(qr[i])
        
    # Oracle: copy x to y
    for i in range(n):
        qc.cx(qr[i], qr[i + n])
        
    # Oracle: apply CNOTs based on the secret string s
    if '1' in s_str:
        first_one = s_str.find('1')
        for i in range(n):
            if s_str[i] == '1':
                qc.cx(qr[first_one], qr[i + n])
                
    # Apply Hadamard gates to the first n qubits
    for i in range(n):
        qc.h(qr[i])
        
    # Measure the first n qubits into the classical register 'c'
    for i in range(n):
        qc.measure(qr[i], cr[i])
        
    return qc
