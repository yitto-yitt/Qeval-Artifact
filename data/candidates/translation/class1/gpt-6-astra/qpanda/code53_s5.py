# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, measure

def xor_gate(a, b):
    prog = QProg()
    for value in (a, b):
        for qubit in range(8):
            if (value >> qubit) & 1:
                prog << X(qubit)

    for qubit in range(8):
        prog << measure(qubit, qubit)

    simulator = CPUQVM()
    result = simulator.run(prog, 1024)
    if not hasattr(result, "get_counts"):
        result = simulator.result()
    counts = result.get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
