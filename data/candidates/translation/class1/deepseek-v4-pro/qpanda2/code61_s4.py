# EVAL_META: task_id=61, framework=qpanda2, class=1
from pyqpanda import *


def create_quantum_circuit_with_one_qubit_and_measure():
    init(QMachineType.CPU)
    q = qAlloc_many(1)
    c = cAlloc_many(1)
    qc = QCircuit()
    qc << Measure(q[0], c[0])
    return qc
