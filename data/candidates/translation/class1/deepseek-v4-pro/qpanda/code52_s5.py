# EVAL_META: task_id=52, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, H, CNOT, X, Z, Measure, init, qAlloc_many, cAlloc_many


def send_bits(bitstring):
    init()
    q = qAlloc_many(2)
    c = cAlloc_many(2)
    circuit = QCircuit()
    circuit << H(q[0]) << CNOT(q[0], q[1])
    if bitstring[1] == "1":
        circuit << Z(q[0])
    if bitstring[0] == "1":
        circuit << X(q[0])
    circuit << CNOT(q[0], q[1]) << H(q[0])
    circuit << Measure(q[0], c[0]) << Measure(q[1], c[1])
    return circuit
