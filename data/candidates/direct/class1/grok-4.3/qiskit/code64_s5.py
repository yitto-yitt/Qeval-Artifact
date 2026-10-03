# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def simons_algorithm(s):
    n = len(s)
    qreg = QuantumRegister(2 * n)
    creg = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qreg, creg)
    for i in range(n):
        qc.h(i)
    for i in range(n):
        qc.cx(i, n + i)
    pivot = -1
    for i in range(n):
        if s[i] == '1':
            pivot = i
            break
    if pivot != -1:
        for i in range(n):
            if s[i] == '1':
                qc.cx(pivot, n + i)
    for i in range(n):
        qc.h(i)
    for i in range(n):
        qc.measure(i, creg[i])
    return qc
