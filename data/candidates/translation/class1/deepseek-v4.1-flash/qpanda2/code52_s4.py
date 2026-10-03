# EVAL_META: task_id=52, framework=qpanda2, class=1
from pyqpanda import QCircuit, QProg, H, X, Z, CNOT, Measure, Qubit, CBit

def send_bits(bitstring):
    q0 = Qubit(0)
    q1 = Qubit(1)
    c0 = CBit(0)
    c1 = CBit(1)
    circuit = QCircuit()
    circuit << H(q0)
    circuit << CNOT(q0, q1)
    if bitstring[1] == "1":
        circuit << Z(q0)
    if bitstring[0] == "1":
        circuit << X(q0)
    circuit << CNOT(q0, q1)
    circuit << H(q0)
    prog = QProg()
    prog << circuit
    prog << Measure(q0, c0)
    prog << Measure(q1, c1)
    return prog
