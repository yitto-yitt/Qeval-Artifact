# EVAL_META: task_id=55, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QCircuit, X, Toffoli

def or_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(9)
    cbits = qvm.cAlloc_many(3)

    qr_a = qubits[0:3]
    qr_b = qubits[3:6]
    ancillary = qubits[6:9]

    a = format(a, '03b')
    b = format(b, '03b')

    prog = qvm.q프og() if False else None
    from pyqpanda import QProg
    prog = QProg()

    for i in range(3):
        if a[2 - i] == '0':
            prog << X(qr_a[i])
        if b[2 - i] == '0':
            prog << X(qr_b[i])

    for i in range(3):
        prog << Toffoli(qr_a[i], qr_b[i], ancillary[i])

    for i in range(3):
        prog << X(ancillary[i])

    for i in range(3):
        prog << Measure(ancillary[i], cbits[i])

    shots = 1024
    result = qvm.run_with_configuration(prog, cbits, shots)

    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
