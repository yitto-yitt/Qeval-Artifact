# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, H, CNOX, CNOT, measure


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    prog = QProg()
    circuit = QCircuit()

    for i in range(n):
        circuit << H(i)

    for i in range(n):
        circuit << CNOT(i, n + i)

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circuit << CNOT(i, n + j)
        for i in range(n):
            circuit << H(i)

    prog << circuit

    for i in range(n):
        prog << measure(i, i)

    return prog
