# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QCircuit, QProg, H

def create_uniform_superposition(n):
    qvm = CPUQVM()
    qvm.init_qvm()
    qv = qvm.qAlloc_many(n)
    circ = QCircuit()
    for i in range(n):
        circ << H(qv[i])
    prog = QProg()
    prog << circ
    qvm.run(prog)
    return qvm.get_qstate()
