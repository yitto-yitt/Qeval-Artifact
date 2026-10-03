# EVAL_META: task_id=71, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, S, U1, CNOT

def create_quantum_circuit_based_h0_csx01_h1():
    q = [0, 1, 2]
    circuit = QCircuit()
    circuit << H(q[0])
    circuit << H(q[1])
    circuit << U1(q[1], -3.141592653589793 / 2)
    circuit << CNOT(q[0], q[1])
    circuit << U1(q[1], 3.141592653589793 / 2)
    circuit << CNOT(q[0], q[1])
    circuit << S(q[1])
    circuit << H(q[1])
    return circuit
