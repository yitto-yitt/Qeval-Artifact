# EVAL_META: task_id=67, framework=qpanda2, class=1
from pyqpanda import *
from numpy import pi


def chsh_circuit(alice, bob):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    circuit = QProg()
    circuit << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    circuit << Barrier(qubits)
    if alice == 0:
        circuit << RY(qubits[0], 0)
    else:
        circuit << RY(qubits[0], -pi / 2)
    circuit << Measure(qubits[0], cbits[0])
    if bob == 0:
        circuit << RY(qubits[1], -pi / 4)
    else:
        circuit << RY(qubits[1], pi / 4)
    circuit << Measure(qubits[1], cbits[1])
    return circuit
