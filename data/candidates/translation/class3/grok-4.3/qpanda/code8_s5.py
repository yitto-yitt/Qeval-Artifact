# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import Parameter, qAlloc, QProg, RX

def rx_gate(value=None):
    theta = Parameter("theta")
    quantum_circuit = QProg()
    q = qAlloc(1)
    quantum_circuit << RX(q[0], theta)
    if value is not None:
        return quantum_circuit.assign_parameters({theta: value})
    return quantum_circuit
