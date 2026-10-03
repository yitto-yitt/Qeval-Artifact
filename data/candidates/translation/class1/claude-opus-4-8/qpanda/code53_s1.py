# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QCircuit, QProg, X, measure

def xor_gate(a, b):
    qvm = CPUQVM()
    n = 8
    qubits = list(range(n))

    circuit = QCircuit()
    val = a ^ b
    for i in range(n):
        if (val >> i) & 1:
            circuit << X(qubits[i])

    prog = QProg()
    prog << circuit
    for i in range(n):
        prog << measure(qubits[i], i)

    qvm.run(prog, 1024)
    counts = qvm.result().get_counts()

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
