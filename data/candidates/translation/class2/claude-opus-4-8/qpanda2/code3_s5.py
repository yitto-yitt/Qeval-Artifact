# EVAL_META: task_id=3, framework=qpanda2, class=2
from pyqpanda import *


def create_ghz(drawing=False):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)

    circuit = QProg()
    circuit << H(qubits[0])
    circuit << CNOT(qubits[0], qubits[1])
    circuit << CNOT(qubits[0], qubits[2])
    circuit << measure_all(qubits, cbits)

    if drawing:
        return circuit, draw_qprog(circuit)
    return circuit
