# EVAL_META: task_id=89, framework=qpanda, class=3
from pyqpanda3.core import QuantumRegister, QCircuit, H

def create_controlled_hgate():
    qr = QuantumRegister(3)
    qc = QCircuit()
    qc << H(qr[2]).control([qr[0], qr[1]])
    return qc
