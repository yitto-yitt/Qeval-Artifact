# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit

def simons_algorithm(s):
    n = len(s)
    qc = QuantumCircuit(2 * n, n)
    qc.h(range(n))
    for i in range(n):
        qc.cx(i, n + i)
    k = None
    for i, bit in enumerate(s):
        if bit == '1':
            k = i
            break
    if k is not None:
        for i in range(n):
            if s[i] == '1':
                qc.cx(k, n + i)
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc
