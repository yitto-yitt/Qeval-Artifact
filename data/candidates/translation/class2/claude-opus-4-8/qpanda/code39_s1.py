# EVAL_META: task_id=39, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import QCircuit, QProg, H, QStat

def create_uniform_superposition(n):
    circ = QCircuit(n)
    for i in range(n):
        circ << H(i)
    prog = QProg()
    prog << circ
    stat = QStat()
    state = stat.state_vector(prog)
    return np.array(state)
