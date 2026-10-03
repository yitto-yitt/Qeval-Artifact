# EVAL_META: task_id=49, framework=qpanda, class=3
from pyqpanda3.core import init, qAlloc_many, QCircuit, H, CNOT

def simple_elitzur_vaidman():
    init()
    qubits = qAlloc_many(2)
    circuit = QCircuit()
    circuit << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << H(qubits[0])
    return circuit
