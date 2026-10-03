# EVAL_META: task_id=54, framework=qpanda2, class=1
from pyqpanda import *

def and_gate(a, b):
    init(QMachineType.CPU)
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(9)
    c = qvm.cAlloc_many(3)

    a_bits = format(a, '03b')
    b_bits = format(b, '03b')

    prog = QProg()

    for i in range(3):
        if a_bits[2 - i] == '1':
            prog << X(q[i])
        if b_bits[2 - i] == '1':
            prog << X(q[3 + i])

    for i in range(3):
        prog << Toffoli(q[i], q[3 + i], q[6 + i])

    for i in range(3):
        prog << Measure(q[6 + i], c[i])

    shots = 1000
    counts = qvm.run_with_configuration(prog, c, shots)

    prob = {}
    for k, v in counts.items():
        bitstr = k.replace(" ", "")
        if len(bitstr) == 3:
            prob[bitstr] = v / shots

    qvm.finalize()
    destroy_quantum_machine(qvm)
    return prob
