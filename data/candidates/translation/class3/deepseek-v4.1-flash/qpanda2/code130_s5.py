# EVAL_META: task_id=130, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(100)

def inv_circuit(n):
    circ = QCircuit()
    circ << CNOT(qubits[2], qubits[4])
    circ << CNOT(qubits[1], qubits[3])
    circ << H(qubits[2])
    circ << H(qubits[1])
    return circ

machine.finalize()
