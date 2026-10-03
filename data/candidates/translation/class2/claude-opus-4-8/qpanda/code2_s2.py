# EVAL_META: task_id=2, framework=qpanda, class=2
import numpy as np
from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, CNOT


def create_bell_statevector():
    qvm = CPUQVM()
    circuit = QCircuit(2)
    circuit << H(0)
    circuit << CNOT(0, 1)

    prog = QProg()
    prog << circuit

    qvm.run(prog, 0)
    return qvm.result().get_state_vector()
