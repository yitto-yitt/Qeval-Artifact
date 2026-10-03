# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import Parameter, QCircuit, RX

def create_parametrized_gate():
    theta = Parameter("theta")
    quantum_circuit = QCircuit()
    q = quantum_circuit.allocateQubits(1)
    quantum_circuit << RX(q[0], theta)
    return quantum_circuit
