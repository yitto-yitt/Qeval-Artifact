# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import *

def and_gate(a, b):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(9)
    c = machine.cAlloc_many(3)

    a_bits = format(a, "03b")
    b_bits = format(b, "03b")

    prog = QProg()

    for i in range(3):
        if a_bits[2 - i] == "1":
            prog << X(q[i])
        if b_bits[2 - i] == "1":
            prog << X(q[3 + i])

    for i in range(3):
        prog << Toffoli(q[i], q[3 + i], q[6 + i])

    for i in range(3):
        prog << Measure(q[6 + i], c[i])

    shots = 1024
    result = machine.run_with_configuration(prog, c, shots)

    total = sum(result.values())
    probs = {k: v / total for k, v in result.items()}

    machine.finalize()
    return probs
