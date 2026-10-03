# EVAL_META: task_id=54, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QCircuit, X, Toffoli

def and_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(9)
    cbits = qvm.cAlloc_many(3)
    qr_a = qubits[0:3]
    qr_b = qubits[3:6]
    ancillary = qubits[6:9]

    a = format(a, '03b')
    b = format(b, '03b')

    prog = qvm.get_qprog() if hasattr(qvm, 'get_qprog') else None
    from pyqpanda import QProg
    prog = QProg()

    for i in range(3):
        if a[2 - i] == '1':
            prog << X(qr_a[i])
        if b[2 - i] == '1':
            prog << X(qr_b[i])

    for i in range(3):
        prog << Toffoli(qr_a[i], qr_b[i], ancillary[i])

    from pyqpanda import measure_all
    prog << measure_all(ancillary, cbits)

    shots = 1024
    counts = qvm.run_with_configuration(prog, cbits, shots)

    total = builtins.sum(counts.values())
    result = {key: value / total for key, value in counts.items()}
    qvm.finalize()
    return result
