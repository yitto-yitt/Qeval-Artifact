# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def simons_algorithm(s):
    n = len(s)
    qr = QuantumRegister(2 * n)
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)
    for i in range(n):
        qc.h(i)
    for i in range(n):
        qc.cx(i, n + i)
    b = s.find('1')
    if b != -1:
        for i in range(n):
            if s[i] == '1':
                qc.cx(i, n + b)
    for i in range(n):
        qc.h(i)
    qc.measure(range(n), range(n))
    return qc
