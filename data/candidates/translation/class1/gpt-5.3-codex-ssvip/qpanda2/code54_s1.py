# EVAL_META: task_id=54, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def and_gate(a, b):
    init(QMachineType.CPU)
    qvm = CPUQVM()
    qvm.init_qvm()
    qr_a = qvm.qAlloc_many(3)
    qr_b = qvm.qAlloc_many(3)
    ancillary = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)

    prog = QProg()

    a_bits = format(a, "03b")
    b_bits = format(b, "03b")

    for i in range(3):
        if a_bits[2 - i] == "1":
            prog << X(qr_a[i])
        if b_bits[2 - i] == "1":
            prog << X(qr_b[i])

    for i in range(3):
        prog << Toffoli(qr_a[i], qr_b[i], ancillary[i])

    for i in range(3):
        prog << Measure(ancillary[i], cbits[i])

    shots = 1024
    counts = qvm.run_with_configuration(prog, cbits, shots)

    qvm.finalize()
    destroy_quantum_machine(qvm)

    total = builtins.sum(counts.values())
    return {k: v / total for k, v in counts.items()}
