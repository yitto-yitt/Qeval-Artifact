# EVAL_META: task_id=3, framework=qpanda2, class=2
from pyqpanda import QCircuit, H, CNOT, Measure, qAlloc_many, cAlloc_many, init, QMachineType


def create_ghz(drawing=False):
    if not getattr(create_ghz, "_initialized", False):
        init(QMachineType.CPU)
        create_ghz._initialized = True

    q = qAlloc_many(3)
    c = cAlloc_many(3)

    qc = QCircuit()
    qc << H(q[0])
    qc << CNOT(q[0], q[1])
    qc << CNOT(q[0], q[2])
    qc << Measure(q[0], c[0])
    qc << Measure(q[1], c[1])
    qc << Measure(q[2], c[2])

    if drawing:
        from pyqpanda import QProg, draw_qprog
        draw_prog = QProg()
        draw_prog << qc
        return qc, draw_qprog(draw_prog)

    return qc
