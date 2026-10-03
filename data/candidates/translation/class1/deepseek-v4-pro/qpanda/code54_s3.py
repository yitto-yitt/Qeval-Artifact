# EVAL_META: task_id=54, framework=qpanda, class=1
try:
    from pyqpanda3.core import init_qvm as _init
except ImportError:
    from pyqpanda3.core import init as _init

from pyqpanda3.core import QMachineType, QProg, qAlloc_many, cAlloc_many, X, Toffoli, Measure, run_with_configuration

_initialized = False


def and_gate(a, b):
    global _initialized
    if not _initialized:
        _init(QMachineType.CPU)
        _initialized = True

    a_bin = format(a, '03b')
    b_bin = format(b, '03b')

    q = qAlloc_many(9)
    c = cAlloc_many(3)

    qr_a = [q[i] for i in range(3)]
    qr_b = [q[i + 3] for i in range(3)]
    anc = [q[i + 6] for i in range(3)]

    prog = QProg()

    for i in range(3):
        if a_bin[2 - i] == '1':
            prog << X(qr_a[i])
        if b_bin[2 - i] == '1':
            prog << X(qr_b[i])

    for i in range(3):
        prog << Toffoli(qr_a[i], qr_b[i], anc[i])

    for i in range(3):
        prog << Measure(anc[i], c[i])

    counts = run_with_configuration(prog, c, 1024)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
