# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT

def inv_circuit(n):
    qc = QCircuit(n)
    qc << H(qc[1])
    qc << H(qc[2])
    qc << CNOT(qc[1], qc[3])
    qc << CNOT(qc[2], qc[4])
    return qc.inverse()
