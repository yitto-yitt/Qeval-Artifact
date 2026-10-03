# EVAL_META: task_id=106, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def compose_cnot_dihedral():
    composed_circ = QCircuit()
    # circ2: CX(0, 1), T(0), X(1)
    # circ1: CX(0, 1), T(0)
    # elem1.compose(elem2) is elem1 * elem2 (circ2 followed by circ1)
    composed_circ << CX(q[0], q[1]) << T(q[0]) << X(q[1]) \
                  << CX(q[0], q[1]) << T(q[0])
    return composed_circ

machine.finalize()
