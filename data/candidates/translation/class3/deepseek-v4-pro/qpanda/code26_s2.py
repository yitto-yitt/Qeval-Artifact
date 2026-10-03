# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit


def bell_dag():
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure(0, 0)
    return qc.to_dag()
