# EVAL_META: task_id=109, framework=qpanda, class=3
from pyqpanda3.core import VariationalQuantumCircuit

try:
    from pyqpanda3.core import var
except ImportError:
    from pyqpanda3.core import Var as var


def circuit():
    qc = VariationalQuantumCircuit(1)
    qc.h(0)
    theta = var('th')
    qc.rz(0, theta)
    return qc
