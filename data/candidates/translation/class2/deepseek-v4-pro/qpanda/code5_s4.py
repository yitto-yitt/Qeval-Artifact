# EVAL_META: task_id=5, framework=qpanda, class=2
from pyqpanda3.core import init_quantum_machine, QMachineType, qAlloc_many, QCircuit, X


def create_state_prep():
    init_quantum_machine(QMachineType.CPU)
    q = qAlloc_many(2)
    qc = QCircuit()
    qc << X(q[0])
    qc << X(q[0])
    qc << X(q[1])
    return qc
