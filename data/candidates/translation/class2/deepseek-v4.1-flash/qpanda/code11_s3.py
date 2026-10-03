# EVAL_META: task_id=11, framework=qpanda, class=2
from pyqpanda3.core import StateVector

def get_statevector(circuit):
    return StateVector(circuit)
