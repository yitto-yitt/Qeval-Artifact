# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def tensor_circuits():
    circuit = QuantumCircuit(3)
    circuit.cry(0.2, 0, 1)
    circuit.x(2)
    return circuit
