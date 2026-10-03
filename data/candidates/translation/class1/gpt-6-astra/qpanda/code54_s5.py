# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, measure


def and_gate(a, b):
    program = QProg()
    a = format(a, "03b")
    b = format(b, "03b")

    for i in range(3):
        if a[2 - i] == "1":
            program << X(i)
        if b[2 - i] == "1":
            program << X(3 + i)

    for i in range(3):
        program << X(6 + i).control([i, 3 + i])

    for i in range(3):
        program << measure(6 + i, i)

    simulator = CPUQVM()
    result = simulator.run(program, 1024)
    if not hasattr(result, "get_counts"):
        result = simulator.result()
    counts = result.get_counts()
    total = sum(counts.values())
    return {key: count / total for key, count in counts.items()}
