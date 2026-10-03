# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, measure


def xor_gate(a, b):
    program = QProg()
    for value in (a, b):
        for i in range(8):
            if (value >> i) & 1:
                program << X(i)

    for i in range(8):
        program << measure(i, i)

    simulator = CPUQVM()
    result = simulator.run(program, 1024)
    if not hasattr(result, "get_counts"):
        result = simulator.result()

    counts = result.get_counts()
    total = sum(counts.values())
    return {key.zfill(8): count / total for key, count in counts.items()}
