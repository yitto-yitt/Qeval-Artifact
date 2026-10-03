# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import (
    CNOT,
    H,
    MeasureAll,
    QMachineType,
    QProg,
    cAlloc_many,
    finalize,
    init,
    qAlloc_many,
    run_with_configuration,
)

def run_bell_state_simulator():
    init(QMachineType.CPU)
    try:
        q = qAlloc_many(2)
        c = cAlloc_many(2)

        prog = QProg()
        prog << H(q[0])
        prog << CNOT(q[0], q[1])
        prog << MeasureAll(q, c)

        counts = run_with_configuration(prog, c, 1000)
        total = sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        finalize()
