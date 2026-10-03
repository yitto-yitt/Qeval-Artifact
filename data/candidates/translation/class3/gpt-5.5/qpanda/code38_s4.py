# EVAL_META: task_id=38, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, RZ, RY, CNOT

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    circuit = QCircuit()
    circuit << H(0)
    circuit << RZ(1, theta / 2)
    circuit << CNOT(0, 1)
    circuit << RZ(1, -theta / 2)
    circuit << CNOT(0, 1)
    circuit << H(1)
    circuit << RY(0, theta / 2)
    circuit << CNOT(1, 0)
    circuit << RY(0, -theta / 2)
    circuit << CNOT(1, 0)
    return circuit
