# EVAL_META: task_id=54, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QCircuit, X, Toffoli

def and_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    qr_a = qvm.qAlloc_many(3)
    qr_b = qvm.qAlloc_many(3)
    ancillary = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)

    a_str = format(a, '03b')
    b_str = format(b, '03b')

    circuit = QCircuit()
    for i in range(3):
        if a_str[2 - i] == '1':
            circuit << X(qr_a[i])
        if b_str[2 - i] == '1':
            circuit << X(qr_b[i])
    for i in range(3):
        circuit << Toffoli(qr_a[i], qr_b[i], ancillary[i])

    prog = qvm.qProg() if hasattr(qvm, 'qProg') else None
    from pyqpanda import QProg, measure_all
    prog = QProg()
    prog << circuit
    prog << measure_all(ancillary, cbits)

    shots = 1024
    counts = qvm.run_with_configuration(prog, cbits, shots)
    qvm.finalize()

    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
