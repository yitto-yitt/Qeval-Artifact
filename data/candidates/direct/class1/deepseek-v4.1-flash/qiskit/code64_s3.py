# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def simons_algorithm(s):
    n = len(s)
    qr = QuantumRegister(2 * n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)
    qc.h(qr[:n])
    k = s.find('1')
    if k == -1:
        for i in range(n):
            qc.cx(qr[i], qr[i + n])
    else:
        for i in range(n):
            qc.cx(qr[i], qr[i + n])
        for i in range(n):
            if s[i] == '1':
                qc.cx(qr[k], qr[i + n])
    qc.h(qr[:n])
    qc.measure(qr[:n], cr)
    return qc
