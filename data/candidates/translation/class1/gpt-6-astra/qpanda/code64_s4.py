# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, measure


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    program = QProg()

    for q in range(n):
        program << H(q)

    for q in range(n):
        program << CNOT(q, n + q)

    if "1" in s:
        pivot = s.find("1")
        for j in range(n):
            if s[j] == "1":
                program << CNOT(pivot, n + j)
        for q in range(n):
            program << H(q)

    for q in range(n):
        program << measure(q, q)

    if n:
        simulator = CPUQVM()
        simulator.run(program, 1)

    return program
