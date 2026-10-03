# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import QMachine, QCircuit, H, CNOT

def inv_circuit(n):
    qm = QMachine()
    qubits = qm.allocate_qubits(n)
    circ = QCircuit()
    for i in range(2):
        circ << H(qubits[i+1])
    for i in range(2):
        circ << CNOT(qubits[i+1], qubits[i+3])
    return circ.dagger()
