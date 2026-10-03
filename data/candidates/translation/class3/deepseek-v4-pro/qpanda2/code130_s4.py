# EVAL_META: task_id=130, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()

def inv_circuit(n):
    q = machine.qAlloc_many(n)
    circ = QCircuit()
    for i in range(2):
        circ << H(q[i + 1])
    for i in range(2):
        circ << CNOT(q[i + 1], q[i + 3])
    return circ.dagger()

machine.finalize()
