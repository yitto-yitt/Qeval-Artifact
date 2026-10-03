# EVAL_META: task_id=106, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

atexit.register(machine.finalize)


def compose_cnot_dihedral():
    circ1 = QCircuit()
    circ1.insert(CNOT(q[0], q[1]))
    circ1.insert(T(q[0]))

    circ2 = QCircuit()
    circ2.insert(CNOT(q[0], q[1]))
    circ2.insert(T(q[0]))
    circ2.insert(X(q[1]))

    composed_circuit = QCircuit()
    composed_circuit.insert(circ1)
    composed_circuit.insert(circ2)

    return composed_circuit
