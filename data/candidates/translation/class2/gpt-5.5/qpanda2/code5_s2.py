# EVAL_META: task_id=5, framework=qpanda2, class=2
from pyqpanda import *


def create_state_prep():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)

    circuit = QCircuit()
    circuit << X(qubits[0])
    circuit << I(qubits[1])

    create_state_prep._qvm = qvm
    create_state_prep._qubits = qubits

    return circuit
