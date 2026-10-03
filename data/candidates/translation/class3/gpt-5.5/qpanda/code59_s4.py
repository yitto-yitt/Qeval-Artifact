# EVAL_META: task_id=59, framework=qpanda, class=3
from pyqpanda3.core import *

def create_cz_gate():
    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    if hasattr(qvm, "qAlloc_many"):
        qubits = qvm.qAlloc_many(2)
    elif hasattr(qvm, "qalloc_many"):
        qubits = qvm.qalloc_many(2)
    else:
        qubits = qvm.allocate_qubits(2)

    circuit = QCircuit()
    circuit << H(qubits[1])
    circuit << CNOT(qubits[0], qubits[1])
    circuit << H(qubits[1])

    if not hasattr(create_cz_gate, "_resources"):
        create_cz_gate._resources = []
    create_cz_gate._resources.append((qvm, qubits))

    return circuit
