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

    s_bits = s[::-1]

    if "1" in s_bits:
        j = s_bits.index("1")
        for i in range(n):
            if i != j:
                qc.cx(x[i], y[i])
        for i, bit in enumerate(s_bits):
            if i != j and bit == "1":
                qc.cx(x[j], y[i])
    else:
        for i in range(n):
            qc.cx(x[i], y[i])

    qc.h(x)
    qc.measure(x, c)

    return qc
