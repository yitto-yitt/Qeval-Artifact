# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, SX

def create_c3sx_circuit():
    circuit = QCircuit()
    qubits = [Qubit(i) for i in range(4)]
    circuit << SX(qubits[3]).control([qubits[0], qubits[1], qubits[2]])
    return circuit
