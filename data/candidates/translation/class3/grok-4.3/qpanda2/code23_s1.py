# EVAL_META: task_id=23, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.initQVM()
qubits = machine.qAlloc_many(3)
def dj_constant_oracle():
    oracle = QCircuit()
    oracle.insert(X(qubits[2]))
    return oracle
machine.finalize()
