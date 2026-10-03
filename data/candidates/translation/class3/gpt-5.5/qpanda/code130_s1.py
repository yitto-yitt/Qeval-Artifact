# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import *

def inv_circuit(n):
    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    else:
        qvm.init()

    qubits = qvm.qAlloc_many(n)
    qc = QCircuit()

    for i in range(1, -1, -1):
        qc.insert(CNOT(qubits[i + 1], qubits[i + 3]))

    for i in range(1, -1, -1):
        qc.insert(H(qubits[i + 1]))

    try:
        qc._qvm = qvm
    except Exception:
        pass

    return qc
