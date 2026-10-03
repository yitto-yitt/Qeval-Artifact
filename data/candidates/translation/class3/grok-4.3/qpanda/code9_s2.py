# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, RY, RZ, CNOT, BARRIER

def create_efficientSU2():
    circuit = QCircuit()
    for i in range(3):
        circuit << RY(i) << RZ(i)
    circuit << BARRIER()
    circuit << CNOT(2, 1) << CNOT(1, 0)
    circuit << BARRIER()
    for i in range(3):
        circuit << RY(i) << RZ(i)
    return circuit
