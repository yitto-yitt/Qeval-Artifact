# EVAL_META: task_id=2, framework=qpanda, class=2
from pyqpanda3.core import StateVector, QCircuit, H, CNOT

def create_bell_statevector():
    circuit = QCircuit()
    circuit << H(0) << CNOT(0, 1)
    return StateVector(circuit)
