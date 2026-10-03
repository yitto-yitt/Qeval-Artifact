# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import QProg, H, CNOT, measure, CPUQVM


def simons_algorithm(s):
    n = len(s)
    secret = s[::-1]
    program = QProg()

    for i in range(n):
        program << H(i)

    for i in range(n):
        program << CNOT(i, n + i)

    if "1" in secret:
        pivot = secret.find("1")
        for j, bit in enumerate(secret):
            if bit == "1":
                program << CNOT(pivot, n + j)

        for i in range(n):
            program << H(i)

    for i in range(n):
        program << measure(i, i)

    if n:
        simulator = CPUQVM()
        simulator.run(program, 1)

    return program
