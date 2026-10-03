# EVAL_META: task_id=9, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, ParameterVector, RY, RZ, CNOT, BARRIER, qAlloc

def create_efficientSU2():
    circuit = QCircuit()
    qubits = qAlloc(3)
    params = ParameterVector("θ", 12)

    # Initial rotation layer
    circuit << RY(qubits[0], params[0]) << RZ(qubits[0], params[1])
    circuit << RY(qubits[1], params[2]) << RZ(qubits[1], params[3])
    circuit << RY(qubits[2], params[4]) << RZ(qubits[2], params[5])
    circuit << BARRIER(qubits)

    # Entanglement layer (full)
    circuit << CNOT(qubits[0], qubits[1])
    circuit << CNOT(qubits[0], qubits[2])
    circuit << CNOT(qubits[1], qubits[2])
    circuit << BARRIER(qubits)

    # Final rotation layer
    circuit << RY(qubits[0], params[6]) << RZ(qubits[0], params[7])
    circuit << RY(qubits[1], params[8]) << RZ(qubits[1], params[9])
    circuit << RY(qubits[2], params[10]) << RZ(qubits[2], params[11])
    circuit << BARRIER(qubits)

    return circuit
