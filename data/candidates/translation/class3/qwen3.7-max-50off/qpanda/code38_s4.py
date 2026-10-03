# EVAL_META: task_id=38, framework=qpanda, class=3
from pyqpanda3.core import QuantumMachine, QCircuit, H, CRZ, CRY

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    qm = QuantumMachine()
    q = qm.qAlloc_many(2)
    circuit = QCircuit()
    circuit << H(q[0])
    circuit << CRZ(q[0], q[1], theta)
    circuit << H(q[1])
    circuit << CRY(q[1], q[0], theta)
    return circuit
