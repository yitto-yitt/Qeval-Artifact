# EVAL_META: task_id=6, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, Qubit, X

def create_state_prep(num_qubits):
    q = Qubit(num_qubits)
    circ = QCircuit()
    circ << X(q[0])
    return circ
