# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, RY, RZ, CNOT, BARRIER, QVar

def create_efficientSU2():
    circuit = QCircuit()
    params = [QVar(f"p{i}") for i in range(6)]
    for i in range(3):
        circuit << RY(i, params[2*i]) << RZ(i, params[2*i+1])
    circuit << BARRIER([0, 1, 2])
    circuit << CNOT(0, 1)
    circuit << CNOT(0, 2)
    circuit << CNOT(1, 2)
    circuit << BARRIER([0, 1, 2])
    return circuit
