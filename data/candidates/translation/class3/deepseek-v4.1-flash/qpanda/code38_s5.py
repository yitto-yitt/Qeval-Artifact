# EVAL_META: task_id=38, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CRZ, CRY, qAlloc

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    qubits = qAlloc(2)
    circuit = QCircuit()
    circuit << H(qubits[0])
    circuit << CRZ(qubits[0], qubits[1], theta)
    circuit << H(qubits[1])
    circuit << CRY(qubits[1], qubits[0], theta)
    return circuit
