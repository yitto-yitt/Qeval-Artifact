# EVAL_META: task_id=13, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, U3
import numpy as np

def custom_rotation_gate():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    circuit = QCircuit()
    circuit << U3(q[0], np.pi / 2, np.pi / 2, np.pi / 2)
    return circuit
