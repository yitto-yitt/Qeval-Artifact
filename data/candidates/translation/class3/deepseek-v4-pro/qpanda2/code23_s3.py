# EVAL_META: task_id=23, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, X

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def dj_constant_oracle():
    oracle = QCircuit()
    oracle << X(qubits[2])
    return oracle

machine.finalize()
