# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import *

def and_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(9)
    c = qvm.cAlloc_many(3)

    a_bits = format(a, "03b")
    b_bits = format(b, "03b")

    prog = QProg()

    # Encode inputs into qr_a (q[0:3]) and qr_b (q[3:6])
    for i in range(3):
        if a_bits[2 - i] == "1":
            prog << X(q[i])
        if b_bits[2 - i] == "1":
            prog << X(q[3 + i])

    # Bitwise AND using Toffoli into ancillary (q[6:9])
    for i in range(3):
        prog << Toffoli(q[i], q[3 + i], q[6 + i])

    # Measure ancillary qubits to classical bits
    for i in range(3):
        prog << Measure(q[6 + i], c[i])

    shots = 1024
    result = qvm.run_with_configuration(prog, c, shots)

    total = sum(result.values())
    probs = {k: v / total for k, v in result.items()}

    qvm.finalize()
    return probs
