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
    prog << H(qubits[1]).control([qubits[0]])
    prog << CNOT(qubits[1], qubits[2])
    prog << CNOT(qubits[0], qubits[1])
    prog << X(qubits[0])
    for i in range(3):
        prog << Measure(qubits[i], cbits[i])
    result = qvm.run_with_configuration(prog, cbits, 1024)
    qvm.finalize()
    return result
