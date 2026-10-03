# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, RX

def rx_gate(value=None):
    theta = value if value is not None else 0.0
    quantum_circuit = QCircuit(1)
    quantum_circuit << RX(0, theta)
    return quantum_circuit
