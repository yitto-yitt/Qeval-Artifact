# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, RY, RZ, CNOT, BARRIER

def create_efficientSU2():
    qubits = [Qubit() for _ in range(3)]
    circuit = QCircuit()

    circuit << BARRIER(qubits)

    for i in range(3):
        circuit << RY(qubits[i], 0.0)
        circuit << RZ(qubits[i], 0.0)

    circuit << BARRIER(qubits)

    circuit << CNOT(qubits[0], qubits[1])
    circuit << CNOT(qubits[0], qubits[2])
    circuit << CNOT(qubits[1], qubits[2])

    circuit << BARRIER(qubits)

    return circuit
