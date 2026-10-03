# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit


def simons_algorithm(s):
    n = len(s)
    qc = QuantumCircuit(2 * n, n)
    qc.add_register(qc.cregs[0])
    qc.cregs[0].name = "c"

    # Input register in superposition
    for i in range(n):
        qc.h(i)

    # Oracle Uf for f(x) = x xor s on second register
    for i, bit in enumerate(s):
        qc.cx(i, n + i)
        if bit == "1":
            qc.x(n + i)

    # Simon-style interference on input register
    for i in range(n):
        qc.h(i)

    # Measure input register to classical register c
    for i in range(n):
        qc.measure(i, i)

    return qc
