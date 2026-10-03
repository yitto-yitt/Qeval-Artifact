# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import Parameter, QCircuit

def create_parametrized_gate():
    theta = Parameter("theta")
    quantum_circuit = QCircuit(1)
    quantum_circuit.rx(theta, 0)
    return quantum_circuit
