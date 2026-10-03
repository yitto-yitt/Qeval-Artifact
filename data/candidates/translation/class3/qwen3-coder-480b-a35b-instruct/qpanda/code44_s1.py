# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda import *

def tensor_circuits():
    # Create the 1-qubit circuit with X gate
    top = QCircuit()
    q1 = QVec([Qubit()])
    top.insert(X(q1[0]))
    
    # Create the 2-qubit circuit with CRY gate
    bottom = QCircuit()
    q2 = QVec([Qubit(), Qubit()])
    bottom.insert(CRY(q2[0], q2[1], 0.2))
    
    # Tensor the circuits (bottom ⊗ top)
    tensored = bottom.tensor(top)
    
    return tensored
