# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import *
def and_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    qr_a = qvm.qAlloc_many(3)
    qr_b = qvm.qAlloc_many(3)
    ancillary = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    prog = QProg()
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    for i in range(3):
        if a_bin[2-i] == '1':
            prog.insert(X(qr_a[i]))
        if b_bin[2-i] == '1':
            prog.insert(X(qr_b[i]))
    for i in range(3):
        prog.insert(Toffoli(qr_a[i], qr_b[i], ancillary[i]))
    prog.insert(measure_all(ancillary, cbits))
    result = qvm.run_with_configuration(prog, cbits, shots=1024)
    counts = result
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
