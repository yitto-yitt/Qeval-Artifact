# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, RY, RZ, CNOT, BARRIER


def create_efficientSU2():
    circuit = QCircuit()
    qubits = [0, 1, 2]

    # Rotation layer 1
    for q in qubits:
        circuit << RY(q, 0.0)
    for q in qubits:
        circuit << RZ(q, 0.0)

    circuit << BARRIER(qubits)

    # Entanglement layer (linear cascade)
    circuit << CNOT(0, 1)
    circuit << CNOT(1, 2)

    circuit << BARRIER(qubits)

    # Rotation layer 2
    for q in qubits:
        circuit << RY(q, 0.0)
    for q in qubits:
        circuit << RZ(q, 0.0)

    return circuit
