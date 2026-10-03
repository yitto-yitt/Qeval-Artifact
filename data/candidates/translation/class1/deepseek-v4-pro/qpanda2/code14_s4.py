# EVAL_META: task_id=14, framework=qpanda2, class=1
import builtins
from pyqpanda import QMachineType, init, qAlloc_many, cAlloc_many, QProg, H, CNOT, Measure, run_with_configuration, finalize

def bell_each_shot():
    init(QMachineType.CPU)
    q = qAlloc_many(2)
    c = cAlloc_many(2)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])

    shots = 10
    counts = run_with_configuration(prog, c, shots=shots)
    finalize()

    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
