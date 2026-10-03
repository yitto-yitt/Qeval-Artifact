# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, Parameter, RX

def rx_gate(value=None):
    theta = Parameter("theta")
    qc = QuantumCircuit()
    qubits = qc.qalloc(1)
    qc << RX(qubits[0], theta)
    if value is not None:
        qc.set_parameter("theta", value)
    return qc
