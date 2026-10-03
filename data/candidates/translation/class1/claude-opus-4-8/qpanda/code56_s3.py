# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, CPUQVM, X, measure

def not_gate(a):
    qvm = CPUQVM()
    circuit = QCircuit(8)
    a = format(a, "08b")
    for i in range(8):
        if a[7 - i] == "0":
            circuit << X(i)
    prog = QProg()
    prog << circuit
    for i in range(8):
        prog << measure(i, i)
    qvm.run(prog, 1024)
    counts = qvm.result().get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
