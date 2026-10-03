# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

def simons_algorithm(s):
    n = len(s)
    qr = QuantumRegister(2 * n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)
    for i in range(n):
        qc.h(i)
    for i in range(n):
        qc.cx(i, n + i)
    if '1' in s:
        b = s.index('1')
        for i in range(n):
            if s[i] == '1':
                qc.cx(i, n + b)
    for i in range(n):
        qc.h(i)
    qc.measure(range(n), cr)
    return qc
