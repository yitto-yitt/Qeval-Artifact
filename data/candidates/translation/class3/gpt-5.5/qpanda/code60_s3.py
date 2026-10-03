# EVAL_META: task_id=60, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import *


def create_cy_gate():
    for make_circuit in (lambda: QCircuit(2), lambda: QCircuit()):
        try:
            circuit = make_circuit()
            circuit << RZ(1, -pi / 2)
            circuit << CNOT(0, 1)
            circuit << RZ(1, pi / 2)
            return circuit
        except Exception:
            pass

    qvm = CPUQVM()
    try:
        qvm.init_qvm()
    except AttributeError:
        qvm.init()

    try:
        qubits = qvm.qAlloc_many(2)
    except AttributeError:
        qubits = qvm.qalloc_many(2)

    circuit = QCircuit()
    circuit << RZ(qubits[1], -pi / 2)
    circuit << CNOT(qubits[0], qubits[1])
    circuit << RZ(qubits[1], pi / 2)
    return circuit
