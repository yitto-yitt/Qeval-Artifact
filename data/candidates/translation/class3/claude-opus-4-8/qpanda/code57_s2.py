# EVAL_META: task_id=57, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CNOT

def create_swap_gate():
    qubits = [0, 1]
    circuit = QCircuit()
    circuit << CNOT(qubits[0], qubits[1])
    circuit << CNOT(qubits[1], qubits[0])
    circuit << CNOT(qubits[0], qubits[1])
    return circuit
