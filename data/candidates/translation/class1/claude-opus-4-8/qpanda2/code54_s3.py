# EVAL_META: task_id=54, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QCircuit, QProg, X, Toffoli

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

    circuit = QCircuit()
    for i in range(3):
        if a[2 - i] == '1':
            circuit << X(qr_a[i])
        if b[2 - i] == '1':
            circuit << X(qr_b[i])
    for i in range(3):
        circuit << Toffoli(qr_a[i], qr_b[i], ancillary[i])

    prog = QProg()
    prog << circuit
    for i in range(3):
        prog << (cbits[i], ancillary[i])

    prog = QProg()
    prog << circuit
    from pyqpanda import measure_all
    prog << measure_all(ancillary, cbits)

    shots = 1024
    counts = qvm.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
