# EVAL_META: task_id=90, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def create_custom_controlled():
    circuit = QCircuit()
    circuit << control(X(q[1]), [q[0], q[3]])
    circuit << control(H(q[2]), [q[0], q[3]])
    return circuit

machine.finalize()
