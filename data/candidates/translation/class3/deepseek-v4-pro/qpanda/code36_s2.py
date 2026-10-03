# EVAL_META: task_id=36, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, Qubit

def bv_function(s):
    n = len(s)
    q = Qubit(n + 1)
    qc = QuantumCircuit(q)
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.cnot(q[index], q[n])
    return qc
