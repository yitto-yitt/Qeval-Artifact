# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, X, H, qalloc

def create_custom_controlled():
    qc1 = QCircuit()
    q_sub = qalloc(2)
    qc1.append(X(q_sub[0]))
    qc1.append(H(q_sub[1]))
    custom = qc1.control(2)
    qc2 = QCircuit()
    q = qalloc(4)
    qc2.append(custom, [q[0], q[3], q[1], q[2]])
    return qc2
