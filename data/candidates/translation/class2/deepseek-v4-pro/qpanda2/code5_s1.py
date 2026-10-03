# EVAL_META: task_id=5, framework=qpanda2, class=2
from pyqpanda import QuantumCircuit


def create_state_prep():
    qc = QuantumCircuit(2)
    qc.prepare_state("01")
    return qc
