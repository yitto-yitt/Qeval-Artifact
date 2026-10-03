# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, RX

def create_parametrized_gate(theta):
    quantum_circuit = QCircuit(1)
    quantum_circuit << RX(0, theta)
    return quantum_circuit
