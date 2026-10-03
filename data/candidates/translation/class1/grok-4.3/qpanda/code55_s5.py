# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, Toffoli, measure
def or_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    qr_a = qvm.allocate_qubits(3)
    qr_b = qvm.allocate_qubits(3)
    ancillary = qvm.allocate_qubits(3)
    cbits = qvm.allocate_cbits(3)
    prog = QProg()
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    for i in range(3):
        if a_bin[2-i] == '0':
            prog.insert(X(qr_a[i]))
        if b_bin[2-i] == '0':
            prog.insert(X(qr_b[i]))
    for i in range(3):
        prog.insert(Toffoli(qr_a[i], qr_b[i], ancillary[i]))
    for i in range(3):
        prog.insert(X(ancillary[i]))
    for i in range(3):
        prog.insert(measure(ancillary[i], cbits[i]))
    result = qvm.run_with_configuration(prog, cbits, 1024)
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
