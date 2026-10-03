# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, H, CNOT

def inv_circuit(n):
    qc = QuantumCircuit()
    qubits = qc.qAllocMany(n)

    for i in range(2):
        qc.insert(H(qubits[i + 1]))

    for i in range(2):
        qc.insert(CNOT(qubits[i + 1], qubits[i + 3]))

    return qc.dagger()
