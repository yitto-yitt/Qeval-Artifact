# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Rx, var

def create_parametrized_gate():
    theta = var(0.0, True, "theta")
    circuit = QCircuit()
    qubits = circuit.allocateQubits(1)
    circuit << Rx(qubits[0], theta)
    return circuit
