# EVAL_META: task_id=67, framework=qpanda, class=1
from math import pi
from pyqpanda3.core import QCircuit, Qubit, CBit, H, CNOT, RY, BARRIER, measure


def chsh_circuit(alice, bob):
    q = [Qubit(0), Qubit(1)]
    c = [CBit(0), CBit(1)]
    circuit = QCircuit()
    circuit << H(q[0])
    circuit << CNOT(q[0], q[1])
    circuit << BARRIER(q)
    if alice == 0:
        circuit << RY(q[0], 0)
    else:
        circuit << RY(q[0], -pi / 2)
    circuit << measure(q[0], c[0])
    if bob == 0:
        circuit << RY(q[1], -pi / 4)
    else:
        circuit << RY(q[1], pi / 4)
    circuit << measure(q[1], c[1])
    return circuit
