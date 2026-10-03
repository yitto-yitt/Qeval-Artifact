# EVAL_META: task_id=6, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, X


def create_state_prep(num_qubits):
    if num_qubits < 1:
        raise ValueError("num_qubits must be positive")

    circuit = QCircuit()
    circuit << X(0)
    for qubit in range(1, num_qubits):
        circuit << X(qubit) << X(qubit)
    return circuit
