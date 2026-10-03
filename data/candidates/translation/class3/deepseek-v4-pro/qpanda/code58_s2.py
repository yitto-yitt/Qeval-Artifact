# EVAL_META: task_id=58, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, RY, CNOT
from math import pi

def create_ch_gate():
    circuit = QuantumCircuit(2)
    circuit << RY(1, pi / 4) << CNOT(0, 1) << RY(1, -pi / 4)
    return circuit
