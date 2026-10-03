# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import QuantumCircuit, QMachine

def create_uniform_superposition(n):
    qc = QuantumCircuit(n)
    for i in range(n):
        qc.h(i)
    qm = QMachine()
    qm.init(n)
    qm.apply(qc)
    return qm.get_state()
