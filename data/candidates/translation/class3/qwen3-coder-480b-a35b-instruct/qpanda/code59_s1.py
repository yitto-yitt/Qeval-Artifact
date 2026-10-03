# EVAL_META: task_id=59, framework=qpanda, class=3
from pyqpanda import *

def create_cz_gate():
    machine = init(QMachineType.CPU)
    qubits = machine.qAlloc_many(2)
    circuit = QCircuit()
    circuit.insert(H(qubits[1]))
    circuit.insert(CNOT(qubits[0], qubits[1]))
    circuit.insert(H(qubits[1]))
    return circuit
