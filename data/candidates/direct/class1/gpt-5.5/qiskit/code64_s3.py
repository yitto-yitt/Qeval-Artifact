# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister


def simons_algorithm(s):
    s = str(s)
    n = len(s)

    x = QuantumRegister(n, "x")
    y = QuantumRegister(n, "y")
    c = ClassicalRegister(n, "c")
    qc = QuantumCircuit(x, y, c)

    hidden = s[::-1]

    qc.h(x)

    for i in range(n):
        qc.cx(x[i], y[i])

    if "1" in hidden:
        pivot = hidden.index("1")
        for j, bit in enumerate(hidden):
            if bit == "1":
                qc.cx(x[pivot], y[j])

    qc.h(x)
    qc.measure(x, c)

    return qc
