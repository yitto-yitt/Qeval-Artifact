# EVAL_META: task_id=67, framework=qpanda, class=1
from numpy import pi
from pyqpanda3.core import QCircuit, Qubit, CBit, H, CNOT, RY, Measure, BARRIER

def chsh_circuit(alice, bob):
    q0 = Qubit(0)
    q1 = Qubit(1)
    c0 = CBit(0)
    c1 = CBit(1)
    circuit = QCircuit()
    circuit << H(q0)
    circuit << CNOT(q0, q1)
    circuit << BARRIER([q0, q1])
    if alice == 0:
        circuit << RY(q0, 0)
    else:
        circuit << RY(q0, -pi / 2)
    circuit << Measure(q0, c0)
    if bob == 0:
        circuit << RY(q1, -pi / 4)
    else:
        circuit << RY(q1, pi / 4)
    circuit << Measure(q1, c1)
    return circuit
