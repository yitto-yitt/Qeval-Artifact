# EVAL_META: task_id=67, framework=qpanda, class=1
from math import pi
from pyqpanda3.core import QuantumCircuit


def chsh_circuit(alice, bob):
    qc = QuantumCircuit()
    qubits = qc.qAllocMany(2)
    cbits = qc.cAllocMany(2)

    qc.h(qubits[0])
    qc.cnot(qubits[0], qubits[1])

    if alice == 0:
        qc.ry(qubits[0], 0.0)
    else:
        qc.ry(qubits[0], -pi / 2)

    qc.measure(qubits[0], cbits[0])

    if bob == 0:
        qc.ry(qubits[1], -pi / 4)
    else:
        qc.ry(qubits[1], pi / 4)

    qc.measure(qubits[1], cbits[1])

    return qc
