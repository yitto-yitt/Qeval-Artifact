# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, measure


def xor_gate(a, b):
    circuit = QProg()
    for value in (a, b):
        for qubit in range(8):
            if (int(value) >> qubit) & 1:
                circuit << X(qubit)

    for qubit in range(8):
        circuit << measure(qubit, qubit)

    backend = CPUQVM()
    backend.run(circuit, 1024)
    counts = backend.result().get_counts()
    total = sum(counts.values())
    return {key.zfill(8): value / total for key, value in counts.items()}
