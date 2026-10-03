# EVAL_META: task_id=53, framework=qpanda2, class=1
import builtins
from pyqpanda import (
    QMachineType,
    QProg,
    X,
    init,
    qAlloc_many,
    cAlloc_many,
    measure_all,
    run_with_configuration,
    destroyQuantumMachine,
)


def xor_gate(a, b):
    init(QMachineType.CPU)
    try:
        q = qAlloc_many(8)
        c = cAlloc_many(8)
        prog = QProg()

        x = a ^ b
        for i in range(8):
            if (x >> i) & 1:
                prog << X(q[i])

        prog << measure_all(q, c)
        counts = run_with_configuration(prog, c, 1024)

        total = builtins.sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        destroyQuantumMachine()
