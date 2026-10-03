# EVAL_META: task_id=39, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import QCircuit, QProg, H, QStat

def create_uniform_superposition(n):
    circuit = QCircuit(n)
    for i in range(n):
        circuit << H(i)
    prog = QProg()
    prog << circuit
    state = QStat()
    state.run(prog)
    return np.array(state.get_qstate())
