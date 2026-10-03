# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def create_unitary_from_matrix():
    circuit = QuantumCircuit(2)
    circuit.cx(1, 0)
    circuit.x(1)
    return circuit
