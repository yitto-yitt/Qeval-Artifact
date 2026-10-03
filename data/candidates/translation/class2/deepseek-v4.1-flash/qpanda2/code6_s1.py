# EVAL_META: task_id=6, framework=qpanda2, class=2
from pyqpanda import QCircuit, X, Qubit

def create_state_prep(num_qubits):
    circuit = QCircuit()
    if num_qubits > 0:
        circuit << X(Qubit(num_qubits - 1))
    return circuit
