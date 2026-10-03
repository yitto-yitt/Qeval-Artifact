# EVAL_META: task_id=14, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def bell_each_shot():
    init(QMachineType.CPU)
    q = qAlloc_many(2)
    c = cAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << MeasureAll(q, c)
    shots = 10
    counts = run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
