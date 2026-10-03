# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, QProg, CNOT, T, X


def compose_cnot_dihedral():
    machine = CPUQVM()
    qubits = machine.qAlloc_many(2)

    circ1 = QCircuit()
    circ1 << CNOT(qubits[0], qubits[1]) << T(qubits[0])

    circ2 = QCircuit()
    circ2 << CNOT(qubits[0], qubits[1]) << T(qubits[0]) << X(qubits[1])

    composed_prog = QProg()
    composed_prog << circ1 << circ2

    compose_cnot_dihedral._machine = machine
    compose_cnot_dihedral._qubits = qubits

    return composed_prog
