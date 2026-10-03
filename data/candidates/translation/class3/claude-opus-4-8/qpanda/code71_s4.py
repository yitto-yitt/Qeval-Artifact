# EVAL_META: task_id=71, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, X

def create_quantum_circuit_based_h0_csx01_h1():
    circuit = QCircuit(3)
    circuit << H(0)
    circuit << X(1).power(0.5).control(0)
    circuit << H(1)
    return circuit
