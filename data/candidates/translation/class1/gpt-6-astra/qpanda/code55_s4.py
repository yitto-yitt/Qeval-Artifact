# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, measure


def or_gate(a, b):
    program = QProg()
    a = format(a, "03b")
    b = format(b, "03b")

    for i in range(3):
        if a[2 - i] == "0":
            program << X(i)
        if b[2 - i] == "0":
            program << X(3 + i)

    for i in range(3):
        program << X(6 + i).control([i, 3 + i])

    for i in range(3):
        program << X(6 + i)

    for i in range(3):
        program << measure(6 + i, i)

    simulator = CPUQVM()
    simulator.run(program, 1024)
    counts = simulator.result().get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
