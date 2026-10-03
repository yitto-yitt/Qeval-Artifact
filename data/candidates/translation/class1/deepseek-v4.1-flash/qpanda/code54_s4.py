# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import QProg, QCircuit, CPUQVM, measure
import pyqpanda3.core as pq

def and_gate(a, b):
    machine = CPUQVM()
    machine.init_qvm()

    qr_a = machine.qAlloc_many(3)
    qr_b = machine.qAlloc_many(3)
    ancillary = machine.qAlloc_many(3)
    measure_qubits = machine.cAlloc_many(3)

    prog = QProg()

    a_bits = format(a, '03b')
    b_bits = format(b, '03b')
    for i in range(3):
        if a_bits[2 - i] == '1':
            prog << pq.X(qr_a[i])
        if b_bits[2 - i] == '1':
            prog << pq.X(qr_b[i])

    for i in range(3):
        prog << pq.Toffoli(qr_a[i], qr_b[i], ancillary[i])

    for i in range(3):
        prog << measure(ancillary[i], measure_qubits[i])

    result = machine.run(prog, 1000)
    counts = result.get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
