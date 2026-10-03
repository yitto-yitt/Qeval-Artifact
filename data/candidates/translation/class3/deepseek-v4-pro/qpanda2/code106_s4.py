# EVAL_META: task_id=106, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)


def compose_cnot_dihedral():
    circ1 = QCircuit()
    circ1 << CNOT(q[0], q[1]) << T(q[0])

    circ2 = QCircuit()
    circ2 << CNOT(q[0], q[1]) << T(q[0]) << X(q[1])

    composed_circuit = QCircuit()
    composed_circuit << CNOT(q[0], q[1]) << T(q[0])
    composed_circuit << CNOT(q[0], q[1]) << T(q[0]) << X(q[1])
    return composed_circuit


machine.finalize()
