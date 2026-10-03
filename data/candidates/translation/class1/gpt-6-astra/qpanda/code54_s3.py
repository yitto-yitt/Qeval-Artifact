# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, measure

def and_gate(a, b):
    circuit = QProg()
    a = format(a, "03b")
    b = format(b, "03b")

    for i in range(3):
        if a[2 - i] == "1":
            circuit << X(i)
        if b[2 - i] == "1":
            circuit << X(3 + i)

    for i in range(3):
        circuit << X(6 + i).control([i, 3 + i])

    for i in range(3):
        circuit << measure(6 + i, i)

    simulator = CPUQVM()
    simulator.run(circuit, 1024)
    counts = simulator.result().get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
