# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, Measure

def not_gate(a):
    qvm = CPUQVM()
    qvm.init()
    qubits = qvm.qAlloc_many(8)
    cbits = qvm.cAlloc_many(8)

    prog = QProg()
    binary = format(a, "08b")
    for i in range(8):
        if binary[7 - i] == "0":
            prog << X(qubits[i])

    for i in range(8):
        prog << Measure(qubits[i], cbits[i])

    counts = qvm.run_with_configuration(prog, cbits, 1024)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
