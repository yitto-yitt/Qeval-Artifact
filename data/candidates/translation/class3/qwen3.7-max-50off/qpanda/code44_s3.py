# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import QProg, QCircuit, Qubit, X, CRY

def tensor_circuits():
    q0 = Qubit()
    q1 = Qubit()
    q2 = Qubit()
    
    bottom = QCircuit()
    bottom << CRY(q0, q1, 0.2)
    
    top = QCircuit()
    top << X(q2)
    
    tensored = QProg()
    tensored << bottom << top
    
    return tensored
