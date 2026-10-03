# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]

    qc = QuantumCircuit(2 * n, n)

    for i in range(n):
        qc.h(i)

    qc.barrier()

    for i in range(n):
        qc.cx(i, n + i)

    if "1" in s:
        control = s.find("1")
        for j in range(n):
            if s[j] == "1":
                qc.cx(control, n + j)

        qc.barrier()

        for i in range(n):
            qc.h(i)

    for i in range(n):
        qc.measure(i, i)

    return qc
