# EVAL_META: task_id=14, framework=qpanda2, class=1
from pyqpanda import *

def bell_each_shot():
    shots = 10
    init(QMachineType.CPU)
    try:
        q = qAlloc_many(2)
        c = cAlloc_many(2)

        prog = QProg()
        prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])

        counts = run_with_configuration(prog, c, shots)
        return {key: value / shots for key, value in counts.items()}
    finally:
        destroyQuantumMachine()
