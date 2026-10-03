# EVAL_META: task_id=66, framework=qpanda, class=2
from numpy import arccos, sqrt
from pyqpanda import *


def w_state():
    machine = init(QMachineType.CPU)
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)
    
    circuit = QCircuit()
    circuit.insert(RY(qubits[0], 2 * arccos(1 / sqrt(3))))
    circuit.insert(CH(qubits[0], qubits[1]))
    circuit.insert(CNOT(qubits[1], qubits[2]))
    circuit.insert(CNOT(qubits[0], qubits[1]))
    circuit.insert(X(qubits[0]))
    
    circuit.insert(Measure(qubits[0], cbits[0]))
    circuit.insert(Measure(qubits[1], cbits[1]))
    circuit.insert(Measure(qubits[2], cbits[2]))
    
    return circuit
