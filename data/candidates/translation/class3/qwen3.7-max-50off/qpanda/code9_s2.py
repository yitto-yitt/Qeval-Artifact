# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import QCircuit

def create_efficientSU2():
    circ = QCircuit()
    
    # Initial rotation layer
    circ.ry(0.0, 0)
    circ.rz(0.0, 0)
    circ.ry(0.0, 1)
    circ.rz(0.0, 1)
    circ.ry(0.0, 2)
    circ.rz(0.0, 2)
    
    circ.barrier()
    
    # Entanglement layer
    circ.cx(0, 1)
    circ.cx(1, 2)
    
    circ.barrier()
    
    # Rep 1 rotation layer
    circ.ry(0.0, 0)
    circ.rz(0.0, 0)
    circ.ry(0.0, 1)
    circ.rz(0.0, 1)
    circ.ry(0.0, 2)
    circ.rz(0.0, 2)
    
    return circ
