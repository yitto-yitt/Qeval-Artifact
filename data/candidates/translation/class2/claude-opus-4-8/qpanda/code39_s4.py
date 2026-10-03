# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, QProg, H, QGate
import numpy as np

def create_uniform_superposition(n):
    circuit = QCircuit(n)
    for i in range(n):
        circuit << H(i)
    prog = QProg()
    prog << circuit
    state = prog.state_vector()
    return np.array(state, dtype=complex)
