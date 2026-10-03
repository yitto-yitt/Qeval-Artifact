# EVAL_META: task_id=130, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(100)

def inv_circuit(n):
    qc = QCircuit()
    for i in range(2):
        qc << H(q[i+1])
    for i in range(2):
        qc << CNOT(q[i+1], q[i+3])
    return qc.dagger()

machine.finalize()
