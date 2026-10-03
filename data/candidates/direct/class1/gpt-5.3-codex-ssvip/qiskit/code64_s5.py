# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit


def simons_algorithm(s):
    n = len(s)
    qc = QuantumCircuit(2 * n, n)
    qc.cregs[0].name = "c"

    for i in range(n):
        qc.h(i)

    for i, bit in enumerate(s):
        if bit == "1":
            qc.cx(i, n + i)

    for i in range(n):
        qc.h(i)

    qc.measure(range(n), range(n))
    return qc
