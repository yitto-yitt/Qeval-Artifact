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

    pivot = None
    for i, bit in enumerate(s):
        if bit == "1":
            pivot = i
            break

    if pivot is not None:
        pivot_q = n - 1 - pivot
        for i, bit in enumerate(s):
            qi = n - 1 - i
            qc.cx(x[qi], y[qi])
            if bit == "1":
                qc.cx(x[pivot_q], y[qi])

    qc.h(x)
    qc.measure(x, c)

    return qc
