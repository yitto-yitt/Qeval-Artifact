# EVAL_META: task_id=0, framework=qpanda, class=3
from pyqpanda3.core import QCircuit

def create_quantum_circuit(n_qubits):
    try:
        return QCircuit(n_qubits)
    except TypeError:
        return QCircuit()
