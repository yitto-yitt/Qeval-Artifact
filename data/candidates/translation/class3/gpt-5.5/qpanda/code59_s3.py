# EVAL_META: task_id=59, framework=qpanda, class=3
from pyqpanda3.core import *


def create_cz_gate():
    qvm = CPUQVM()
    if hasattr(qvm, "init"):
        qvm.init()
    elif hasattr(qvm, "init_qvm"):
        qvm.init_qvm()

    if hasattr(qvm, "qAlloc_many"):
        qubits = qvm.qAlloc_many(2)
    else:
        qubits = qvm.qAllocMany(2)

    circuit = QCircuit()
    circuit << H(qubits[1])
    circuit << CNOT(qubits[0], qubits[1])
    circuit << H(qubits[1])

    if not hasattr(create_cz_gate, "_qpanda_resources"):
        create_cz_gate._qpanda_resources = []
    create_cz_gate._qpanda_resources.append((qvm, qubits))

    return circuit
