# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import *

def create_efficientSU2():
    circuit = QCircuit(3)
    params = [Parameter(f"θ_{i}") for i in range(12)]
    for q in range(3):
        circuit << RY(params[2*q], q) << RZ(params[2*q+1], q)
    circuit << barrier()
    circuit << CNOT(0, 1) << CNOT(1, 2)
    circuit << barrier()
    for q in range(3):
        circuit << RY(params[6+2*q], q) << RZ(params[6+2*q+1], q)
    return circuit
