# EVAL_META: task_id=14, framework=qpanda2, class=1
from pyqpanda import *

def bell_each_shot():
    init(QMachineType.CPU)
    q = qAlloc_many(2)
    c = cAlloc_many(2)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << MeasureAll(q, c)

    shots = 10
    counts = run_with_configuration(prog, c, shots)
    finalize()

    return {bitstring: count / shots for bitstring, count in counts.items()}
