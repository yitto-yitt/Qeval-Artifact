# EVAL_META: task_id=54, framework=qpanda2, class=1
from pyqpanda import (
    QMachineType,
    QProg,
    qAlloc_many,
    cAlloc_many,
    X,
    Toffoli,
    Measure,
    init,
    run_with_configuration
)

def and_gate(a, b):
    init(QMachineType.CPU)

    qr_a = qAlloc_many(3)
    qr_b = qAlloc_many(3)
    anc = qAlloc_many(3)
    creg = cAlloc_many(3)

    prog = QProg()

    a_bin = format(a, '03b')
    b_bin = format(b, '03b')

    for i in range(3):
        if a_bin[2 - i] == '1':
            prog << X(qr_a[i])
        if b_bin[2 - i] == '1':
            prog << X(qr_b[i])

    for i in range(3):
        prog << Toffoli(qr_a[i], qr_b[i], anc[i])

    for i in range(3):
        prog << Measure(anc[i], creg[i])

    cbits_qiskit_order = [creg[2], creg[1], creg[0]]
    shots = 1000
    counts = run_with_configuration(prog, cbits_qiskit_order, shots)

    return {key: value / shots for key, value in counts.items()}
