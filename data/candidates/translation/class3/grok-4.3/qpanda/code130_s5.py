# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import *

def inv_circuit(n):
    qubits = qAlloc_many(n)
    circuit = QCircuit()
    circuit << H(qubits[1]) << H(qubits[2])
    circuit << CNOT(qubits[1], qubits[3]) << CNOT(qubits[2], qubits[4])
    return circuit.inverse()
