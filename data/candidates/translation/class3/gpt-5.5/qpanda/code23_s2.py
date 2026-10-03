# EVAL_META: task_id=23, framework=qpanda, class=3
from pyqpanda3.core import *

def dj_constant_oracle():
    try:
        oracle = QCircuit(3)
    except TypeError:
        oracle = QCircuit()
    try:
        oracle << X(2)
        return oracle
    except Exception:
        qvm = CPUQVM()
        if hasattr(qvm, "init_qvm"):
            qvm.init_qvm()
        elif hasattr(qvm, "init"):
            qvm.init()
        qubits = qvm.qAlloc_many(3)
        oracle = QCircuit()
        oracle << X(qubits[2])
        return oracle
