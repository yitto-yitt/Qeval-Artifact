# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, CPUQVM, X, Toffoli, measure

def and_gate(a, b):
    qvm = CPUQVM()
    prog = QProg()
    circuit = QCircuit()
    a = format(a, '03b')
    b = format(b, '03b')
    for i in range(3):
        if a[2 - i] == '1':
            circuit << X(i)
        if b[2 - i] == '1':
            circuit << X(3 + i)
    for i in range(3):
        circuit << Toffoli(i, 3 + i, 6 + i)
    prog << circuit
    for i in range(3):
        prog << measure(6 + i, i)
    qvm.run(prog, 1000)
    counts = qvm.result().get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
