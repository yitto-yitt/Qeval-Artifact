# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, measure


def xor_gate(a, b):
    program = QProg()
    for value in (a, b):
        for qubit in range(8):
            if (value >> qubit) & 1:
                program << X(qubit)

    for qubit in range(8):
        program << measure(qubit, qubit)

    simulator = CPUQVM()
    simulator.run(program, 1024)
    counts = simulator.result().get_counts()
    total = sum(counts.values())
    return {key.zfill(8): count / total for key, count in counts.items()}
