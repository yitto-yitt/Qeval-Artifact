# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, measure


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    circuit = QProg()

    for j in range(n):
        circuit << H(j)

    for j in range(n):
        circuit << CNOT(j, n + j)

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circuit << CNOT(i, n + j)

        for j in range(n):
            circuit << H(j)

    for j in range(n):
        circuit << measure(j, j)

    if n:
        simulator = CPUQVM()
        simulator.run(circuit, 1)

    return circuit
