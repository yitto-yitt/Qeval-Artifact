# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit

def simons_algorithm(s):
    n = len(s)
    qc = QuantumCircuit(n * 2, n)
    qc.h(range(n))
    qc.barrier()
    for i in range(n):
        qc.cx(i, n + i)
    if '1' in s:
        k = s.index('1')
        for i in range(n):
            if s[i] == '1':
                qc.cx(k, n + i)
    qc.barrier()
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc
