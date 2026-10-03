# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def simons_algorithm(s):
    n = len(s)
    qr_input = QuantumRegister(n, 'x')
    qr_output = QuantumRegister(n, 'y')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr_input, qr_output, cr)
    
    qc.h(qr_input)
    
    if '1' not in s:
        for i in range(n):
            qc.cx(qr_input[i], qr_output[i])
    else:
        j = s.find('1')
        for i in range(n):
            if i != j and s[i] == '1':
                qc.cx(qr_input[j], qr_input[i])
        for i in range(n):
            if i != j:
                qc.cx(qr_input[i], qr_output[i])
        for i in range(n):
            if i != j and s[i] == '1':
                qc.cx(qr_input[j], qr_input[i])
                
    qc.h(qr_input)
    qc.measure(qr_input, cr)
    
    return qc
