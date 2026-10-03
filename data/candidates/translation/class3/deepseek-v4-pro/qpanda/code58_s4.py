# EVAL_META: task_id=58, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit
from numpy import pi

def create_ch_gate():
    circuit = QuantumCircuit(2)
    circuit.ry(1, pi/4)
    circuit.cnot(0, 1)
    circuit.ry(1, -pi/4)
    return circuit
