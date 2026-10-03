# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, measure

def not_gate(a):
    program = QProg()
    bits = format(a, "08b")
    for i in range(8):
        if bits[7 - i] == "0":
            program << X(i)
    for i in range(8):
        program << measure(i, i)

    simulator = CPUQVM()
    simulator.run(program, 1024)
    counts = simulator.result().get_counts()
    total = sum(counts.values())
    return {key.zfill(8): value / total for key, value in counts.items()}
