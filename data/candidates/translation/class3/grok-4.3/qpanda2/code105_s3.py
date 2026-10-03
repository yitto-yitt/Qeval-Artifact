# EVAL_META: task_id=105, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
q = qAlloc_many(2)
def initialize_cnot_dihedral():
    circ = QCircuit()
    circ << CNOT(q[0], q[1])
    circ << T(q[0])
    return circ
machine.finalize()
