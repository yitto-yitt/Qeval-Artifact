# EVAL_META: task_id=56, framework=qpanda2, class=1
from pyqpanda import *

def not_gate(a):
    machine = CPUQVM()
    machine.init_qvm()
    try:
        q = machine.qAlloc_many(8)
        c = machine.cAlloc_many(8)
        prog = QProg()
        bits = format(a, "08b")
        for i in range(8):
            if bits[7 - i] == "0":
                prog << X(q[i])
        for i in range(8):
            prog << Measure(q[i], c[i])
        shots = 1024
        counts = machine.run_with_configuration(prog, c, shots)
        return {key: value / shots for key, value in counts.items()}
    finally:
        machine.finalize()
