# EVAL_META: task_id=39, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import QCircuit, QProg, H, QuantumStateTomography
from pyqpanda3.core import CPUQVM


def create_uniform_superposition(n):
    circ = QCircuit()
    for i in range(n):
        circ << H(i)
    prog = QProg()
    prog << circ

    qvm = CPUQVM()
    qvm.run(prog, 0)
    state = qvm.result().get_state_vector()
    return np.array(state)
