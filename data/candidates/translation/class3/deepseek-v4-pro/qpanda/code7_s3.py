# EVAL_META: task_id=7, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import *

def create_parametrized_gate():
    init(QuantumMachineType.CPU)
    q = qAlloc_many(1)
    theta = var(np.array([0.0]), True)
    quantum_circuit = QCircuit()
    quantum_circuit << RX(q[0], theta[0])
    return quantum_circuit
