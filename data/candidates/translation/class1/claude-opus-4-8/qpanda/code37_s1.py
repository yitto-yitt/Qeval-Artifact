# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, QCircuit, H, X, CNOT, measure


def bv_algorithm(s):
    n = len(s)
    ancilla = n

    circ = QCircuit()
    circ << X(ancilla)
    for i in range(n + 1):
        circ << H(i)
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circ << CNOT(index, ancilla)
    for i in range(n):
        circ << H(i)

    prog = QProg()
    prog << circ
    for i in range(n):
        prog << measure(i, i)

    qvm = CPUQVM()
    qvm.run(prog, 1)
    res = qvm.result().get_counts()

    bitstrings = []
    for key, count in res.items():
        key = key[-n:] if len(key) >= n else key.zfill(n)
        for _ in range(count):
            bitstrings.append(key)

    return [bitstrings, res]
