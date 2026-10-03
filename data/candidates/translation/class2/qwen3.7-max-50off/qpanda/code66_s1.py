# EVAL_META: task_id=66, framework=qpanda, class=2
from pyqpanda3.core import QuantumCircuit
from numpy import arccos, sqrt, pi

def w_state():
    circuit = QuantumCircuit(3)
    theta = 2 * arccos(1 / sqrt(3))
    
    circuit.ry(0, theta)
    
    # CH(0, 1) decomposition
    circuit.ry(1, pi / 4)
    circuit.cx(0, 1)
    circuit.ry(1, -pi / 4)
    
    circuit.cx(1, 2)
    circuit.cx(0, 1)
    circuit.x(0)
    
    circuit.measure_all()
    return circuit
