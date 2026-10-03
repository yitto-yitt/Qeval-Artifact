# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def simons_algorithm(s):
    n = len(s)
    qr = QuantumRegister(2 * n, 'q')
    cr = ClassicalRegister(n, 'c')
    qc = QuantumCircuit(qr, cr)

    qc.h(range(n))
    qc.barrier()

    for i in range(n):
        qc.cx(i, n + i)

    j = s.find('1')
    if j != -1:
        for i in range(n):
            if s[i] == '1':
                qc.cx(j, n + i)

    qc.barrier()
    qc.h(range(n))
    qc.barrier()

    qc.measure(range(n), range(n))

    return qc
