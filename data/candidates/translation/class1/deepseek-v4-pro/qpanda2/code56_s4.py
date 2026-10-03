# EVAL_META: task_id=56, framework=qpanda2, class=1
from pyqpanda import *

def not_gate(a):
    init(QMachineType.CPU)
    q = qAlloc_many(8)
    c = cAlloc_many(8)
    prog = QProg()
    a_bin = format(a, "08b")
    for i in range(8):
        if a_bin[i] == "0":
            prog << X(q[i])
    prog << measure_all(q, c)
    shots = 1024
    counts = run_with_configuration(prog, c, shots)
    result = {key: value / shots for key, value in counts.items()}
    destroyQuantumMachine()
    return result
