# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda3.core import *

def create_c3sx_circuit():
    init(QuantumMachineType.CPU)
    qubits = qalloc(4)
    circuit = QCircuit()
    circuit << C3SX(qubits[0], qubits[1], qubits[2], qubits[3])
    return circuit
