# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, H, CNOT

def inv_circuit(n):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(n)
    qc = QCircuit()
    for i in range(2):
        qc << H(q[i+1])
    for i in range(2):
        qc << CNOT(q[i+1], q[i+3])
    return qc.dagger()
