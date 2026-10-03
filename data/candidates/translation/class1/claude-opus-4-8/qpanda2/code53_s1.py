# EVAL_META: task_id=53, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QCircuit, X, measure_all

def xor_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(8)
    cbits = qvm.cAlloc_many(8)

    prog = qvm.qProg() if hasattr(qvm, "qProg") else None

    from pyqpanda import QProg
    prog = QProg()

    circ = QCircuit()
    c = a ^ b
    for i in range(8):
        if (c >> i) & 1:
            circ << X(qubits[i])

    prog << circ << measure_all(qubits, cbits)

    shots = 1024
    counts = qvm.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
