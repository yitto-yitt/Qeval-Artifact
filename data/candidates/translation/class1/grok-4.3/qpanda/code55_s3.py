# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import *
def or_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    qr_a = qvm.qAlloc_many(3)
    qr_b = qvm.qAlloc_many(3)
    ancillary = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    prog = QProg()
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    for i in range(3):
        if a_str[2-i] == '0':
            prog << X(qr_a[i])
        if b_str[2-i] == '0':
            prog << X(qr_b[i])
    for i in range(3):
        prog << Toffoli(qr_a[i], qr_b[i], ancillary[i])
    for i in range(3):
        prog << X(ancillary[i])
    prog << measure_all(ancillary, cbits)
    result = qvm.run_with_configuration(prog, shots=1024)
    counts = result if isinstance(result, dict) else result.get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
