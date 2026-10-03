# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import *

def create_parametrized_gate():
    init_quantum_machine(QMachineType.CPU)
    q = qAlloc_many(1)
    theta = var(0.0)
    circuit = QCircuit()
    circuit << RX(q[0], theta)
    return circuit
