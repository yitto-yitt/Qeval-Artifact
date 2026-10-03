# EVAL_META: task_id=49, framework=qpanda, class=3
from pyqpanda3.core import *

_KEEPALIVE = []

def simple_elitzur_vaidman():
    try:
        circuit = QCircuit(2)
        circuit << H(0)
        circuit << CNOT(0, 1)
        circuit << H(0)
        return circuit
    except Exception:
        pass

    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    qubits = qvm.qAlloc_many(2)
    circuit = QCircuit()
    circuit << H(qubits[0])
    circuit << CNOT(qubits[0], qubits[1])
    circuit << H(qubits[0])

    _KEEPALIVE.append(qvm)
    return circuit
