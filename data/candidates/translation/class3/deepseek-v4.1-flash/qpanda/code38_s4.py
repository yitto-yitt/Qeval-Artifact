# EVAL_META: task_id=38, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CRZ, CRY

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    circuit = QCircuit(2)
    circuit << H(0)
    circuit << CRZ(0, 1, theta)
    circuit << H(1)
    circuit << CRY(1, 0, theta)
    return circuit
