# EVAL_META: task_id=23, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, X

def dj_constant_oracle():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    oracle = QCircuit()
    oracle << X(qubits[2])
    return oracle
