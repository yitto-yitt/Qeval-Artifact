# EVAL_META: task_id=109, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def circuit():
    qc = QCircuit()
    qc << H(qubits[0])
    qc << RZ(qubits[0], Var(0))
    return qc

machine.finalize()
