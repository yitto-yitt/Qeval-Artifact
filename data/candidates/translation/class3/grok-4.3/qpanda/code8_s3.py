# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import Parameter, QCircuit

def rx_gate(value=None):
    theta = Parameter("theta")
    quantum_circuit = QCircuit(1)
    quantum_circuit.rx(theta, 0)
    if value is not None:
        return quantum_circuit.assign_parameters({theta: value})
    return quantum_circuit
