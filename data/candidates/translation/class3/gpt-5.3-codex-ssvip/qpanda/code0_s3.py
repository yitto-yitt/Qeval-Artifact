# EVAL_META: task_id=0, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, qalloc_many

def create_quantum_circuit(n_qubits):
    q = qalloc_many(n_qubits)
    circ = QCircuit()
    return circ
