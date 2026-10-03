# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, qAlloc_many, H, CNOT, U1
from math import pi

def create_c3sx_circuit():
    q = qAlloc_many(4)
    circuit = QCircuit()
    circuit << H(q[3])
    circuit << U1(q[3], pi/4)
    circuit << CNOT(q[2], q[3])
    circuit << U1(q[3], -pi/4)
    circuit << CNOT(q[1], q[3])
    circuit << U1(q[3], pi/4)
    circuit << CNOT(q[2], q[3])
    circuit << U1(q[3], -pi/4)
    circuit << CNOT(q[0], q[3])
    circuit << U1(q[3], pi/4)
    circuit << CNOT(q[2], q[3])
    circuit << U1(q[3], -pi/4)
    circuit << CNOT(q[1], q[3])
    circuit << U1(q[3], pi/4)
    circuit << CNOT(q[2], q[3])
    circuit << U1(q[3], -pi/4)
    circuit << H(q[3])
    return circuit
