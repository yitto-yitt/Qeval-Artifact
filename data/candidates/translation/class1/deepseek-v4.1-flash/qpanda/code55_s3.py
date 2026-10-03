# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, CPUQVM, X, CCX, measure

def or_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()

    qr_a = qvm.qAlloc_many(3)
    qr_b = qvm.qAlloc_many(3)
    ancillary = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)

    circ = QCircuit()
    a_str = format(a, '03b')
    b_str = format(b, '03b')

    for i in range(3):
        if a_str[2 - i] == '0':
            circ << X(qr_a[i])
        if b_str[2 - i] == '0':
            circ << X(qr_b[i])

    for i in range(3):
        circ << CCX(qr_a[i], qr_b[i], ancillary[i])

    for i in range(3):
        circ << X(ancillary[i])

    prog = QProg()
    prog << circ

    for i in range(3):
        prog << measure(ancillary[i], c[i])

    shots = 1024
    result = qvm.run_with_configuration(prog, c, shots)
    qvm.finalize()

    total = sum(result.values())
    dist = {}
    for key, count in result.items():
        qiskit_key = key[::-1]
        dist[qiskit_key] = count / total
    return dist
