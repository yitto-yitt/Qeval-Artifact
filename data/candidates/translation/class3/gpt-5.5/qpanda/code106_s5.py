# EVAL_META: task_id=106, framework=qpanda, class=3
from pyqpanda3.core import *


def compose_cnot_dihedral():
    qvm = CPUQVM()
    for name in ("init", "init_qvm"):
        method = getattr(qvm, name, None)
        if callable(method):
            method()
            break

    qubits = None
    for name in ("qAlloc_many", "qalloc_many", "qAllocMany", "qallocMany"):
        method = getattr(qvm, name, None)
        if callable(method):
            qubits = method(2)
            break
    if qubits is None:
        alloc = getattr(qvm, "qAlloc", None) or getattr(qvm, "qalloc", None)
        qubits = [alloc(), alloc()]

    circ1 = QCircuit()
    circ1 << CNOT(qubits[0], qubits[1])
    circ1 << T(qubits[0])

    circ2 = QCircuit()
    circ2 << CNOT(qubits[0], qubits[1])
    circ2 << T(qubits[0])
    circ2 << X(qubits[1])

    composed_prog = QProg()
    composed_prog << circ1
    composed_prog << circ2

    compose_cnot_dihedral._qvm = qvm
    compose_cnot_dihedral._qubits = qubits

    return composed_prog
