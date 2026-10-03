# EVAL_META: task_id=66, framework=qpanda2, class=2
from numpy import arccos, sqrt
from pyqpanda import *

def w_state():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    prog = QProg()
    prog << RY(qubits[0], 2 * arccos(1 / sqrt(3)))
    h_gate = H(qubits[1])
    prog << h_gate.control(qubits[0])
    prog << CNOT(qubits[1], qubits[2])
    prog << CNOT(qubits[0], qubits[1])
    prog << X(qubits[0])
    prog << Measure(qubits[0], cbits[0]) << Measure(qubits[1], cbits[1]) << Measure(qubits[2], cbits[2])
    result = qvm.run_with_configuration(prog, cbits, 1024)
    return result
