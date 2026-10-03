# EVAL_META: task_id=59, framework=qpanda, class=3
from pyqpanda3.core import QuantumMachine, QCircuit, H, CNOT

def create_cz_gate():
    qm = QuantumMachine()
    qubits = qm.allocateQubits(2)
    circuit = QCircuit()
    circuit << H(qubits[1]) << CNOT(qubits[0], qubits[1]) << H(qubits[1])
    return circuit
