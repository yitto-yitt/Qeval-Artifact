# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, CPUQVM, X, Toffoli, measure

def or_gate(a, b):
    a = format(a, '03b')
    b = format(b, '03b')

    circuit = QCircuit()
    for i in range(3):
        if a[2 - i] == '0':
            circuit << X(i)
        if b[2 - i] == '0':
            circuit << X(3 + i)
    for i in range(3):
        circuit << Toffoli(i, 3 + i, 6 + i)
    for i in range(3):
        circuit << X(6 + i)

    prog = QProg()
    prog << circuit
    for i in range(3):
        prog << measure(6 + i, i)

    qvm = CPUQVM()
    qvm.run(prog, 1024)
    counts = qvm.result().get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
