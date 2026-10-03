# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def simons_algorithm(s):
    s = str(s)
    n = len(s)

    x = QuantumRegister(n, "x")
    y = QuantumRegister(n, "y")
    c = ClassicalRegister(n, "c")
    qc = QuantumCircuit(x, y, c)

    qc.h(x)

    for i in range(n):
        qc.cx(x[i], y[i])

    if "1" in s:
        pivot = s.index("1")
        for i, bit in enumerate(s):
            if bit == "1":
                qc.cx(x[pivot], y[i])

    qc.h(x)
    qc.measure(x, c)

    return qc
