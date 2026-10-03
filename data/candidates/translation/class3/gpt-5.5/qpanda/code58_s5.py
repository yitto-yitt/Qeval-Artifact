# EVAL_META: task_id=58, framework=qpanda, class=3
from pyqpanda3.core import *
from math import pi

def create_ch_gate():
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
        qubits = [qvm.qAlloc(), qvm.qAlloc()]

    circuit = QCircuit()
    circuit << RY(qubits[1], pi / 4)
    if "CNOT" in globals():
        circuit << CNOT(qubits[0], qubits[1])
    else:
        circuit << CX(qubits[0], qubits[1])
    circuit << RY(qubits[1], -pi / 4)

    if not hasattr(create_ch_gate, "_resources"):
        create_ch_gate._resources = []
    create_ch_gate._resources.append((qvm, qubits))

    return circuit
