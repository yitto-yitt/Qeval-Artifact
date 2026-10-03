# EVAL_META: task_id=38, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT, RY, RZ, qAlloc_many

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    qubits = qAlloc_many(2)
    qc = QCircuit()
    qc << H(qubits[0])
    qc << RZ(qubits[1], theta / 2)
    qc << CNOT(qubits[0], qubits[1])
    qc << RZ(qubits[1], -theta / 2)
    qc << CNOT(qubits[0], qubits[1])
    qc << H(qubits[1])
    qc << RY(qubits[0], theta / 2)
    qc << CNOT(qubits[1], qubits[0])
    qc << RY(qubits[0], -theta / 2)
    qc << CNOT(qubits[1], qubits[0])
    return qc
