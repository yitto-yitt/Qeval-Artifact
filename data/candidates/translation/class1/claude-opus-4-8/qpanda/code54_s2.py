# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, CPUQVM, X, Toffoli, measure

def and_gate(a, b):
    qr_a = [0, 1, 2]
    qr_b = [3, 4, 5]
    ancillary = [6, 7, 8]
    a = format(a, '03b')
    b = format(b, '03b')
    circuit = QCircuit()
    for i in range(3):
        if a[2 - i] == '1':
            circuit << X(qr_a[i])
        if b[2 - i] == '1':
            circuit << X(qr_b[i])
    for i in range(3):
        circuit << Toffoli(qr_a[i], qr_b[i], ancillary[i])
    prog = QProg()
    prog << circuit
    for i in range(3):
        prog << measure(ancillary[i], i)
    qvm = CPUQVM()
    result = qvm.run(prog, 1024)
    counts = result.get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
