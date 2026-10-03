# EVAL_META: task_id=49, framework=qpanda, class=3
from pyqpanda3.core import *

def simple_elitzur_vaidman():
    machine = init(QMachineType.CPU)
    qubits = machine.qAlloc_many(2)
    circuit = QCircuit()
    circuit.insert(H(qubits[0]))
    circuit.insert(CNOT(qubits[0], qubits[1]))
    circuit.insert(H(qubits[0]))
    return circuit
