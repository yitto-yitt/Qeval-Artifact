# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def simons_algorithm(s):
    n = len(s)
    qr = QuantumRegister(2 * n, "q")
    cr = ClassicalRegister(n, "c")
    qc = QuantumCircuit(qr, cr)

    qc.h(range(n))
    qc.barrier()

    b = s[::-1]
    for q in range(n):
        qc.cx(q, q + n)

    if '1' in b:
        i = b.find('1')
        for q in range(n):
            if b[q] == '1':
                qc.cx(i, q + n)

    qc.barrier()
    qc.h(range(n))
    qc.measure(range(n), range(n))

    return qc
