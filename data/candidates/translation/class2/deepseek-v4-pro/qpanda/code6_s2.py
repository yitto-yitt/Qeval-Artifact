# EVAL_META: task_id=6, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, X, AllocateQubits


def create_state_prep(num_qubits):
    qubits = AllocateQubits(num_qubits)
    circuit = QCircuit()
    circuit << X(qubits[0])
    return circuit
