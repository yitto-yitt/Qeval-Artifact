# EVAL_META: task_id=36, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QuantumRegister, CNOT

def bv_function(s):
    n = len(s)
    qr = QuantumRegister(n + 1)
    qc = QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.insert(CNOT(qr[index], qr[n]))
    return qc
