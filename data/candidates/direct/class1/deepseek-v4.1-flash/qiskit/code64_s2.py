# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def simons_algorithm(s):
    n = len(s)
    qr = QuantumRegister(2 * n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)

    for i in range(n):
        qc.h(qr[i])

    for i in range(n):
        qc.cx(qr[i], qr[n + i])

    k = None
    for i, bit in enumerate(s):
        if bit == '1':
            k = i
            break

    if k is not None:
        for i, bit in enumerate(s):
            if bit == '1':
                qc.cx(qr[k], qr[n + i])

    for i in range(n):
        qc.h(qr[i])

    for i in range(n):
        qc.measure(qr[i], cr[i])

    return qc
