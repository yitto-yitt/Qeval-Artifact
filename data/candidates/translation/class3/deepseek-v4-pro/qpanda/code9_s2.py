# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import QPandaInit, QCircuit, RY, RZ, CNOT, barrier, var

def create_efficientSU2():
    init = QPandaInit()
    qvm = init.quantum_machine()
    qubits = qvm.qAlloc(3)

    circuit = QCircuit()

    circuit << barrier(qubits)

    for i in range(3):
        circuit << RY(qubits[i], var(0.0))
    for i in range(3):
        circuit << RZ(qubits[i], var(0.0))

    circuit << CNOT(qubits[0], qubits[1])
    circuit << CNOT(qubits[0], qubits[2])
    circuit << CNOT(qubits[1], qubits[2])

    circuit << barrier(qubits)

    return circuit
