# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT, qAlloc

def inv_circuit(n):
    qubits = qAlloc(n)
    circuit = QCircuit()
    for i in range(2):
        circuit << H(qubits[i + 1])
    for i in range(2):
        circuit << CNOT(qubits[i + 1], qubits[i + 3])
    return circuit.dagger()
