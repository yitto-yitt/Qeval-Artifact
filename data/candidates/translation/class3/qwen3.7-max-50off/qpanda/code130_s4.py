# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3 import QuantumCircuit, H, CNOT

def inv_circuit(n):
    qc = QuantumCircuit(n)
    qc << H(1)
    qc << H(2)
    qc << CNOT(1, 3)
    qc << CNOT(2, 4)
    return qc.dagger()
