# EVAL_META: task_id=109, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def circuit():
    qc = QCircuit()
    qc << H(qubits[0])
    theta = machine.allocate_var('th')
    qc << RZ(qubits[0], theta)
    return qc

machine.finalize()
