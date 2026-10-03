# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, QVec, X, H

def create_custom_controlled():
    q = [Qubit(i) for i in range(4)]
    custom = QCircuit()
    custom << X(q[1])
    custom << H(q[2])
    ctrl = QVec()
    ctrl.append(q[0])
    ctrl.append(q[3])
    controlled = custom.control(ctrl)
    return controlled
