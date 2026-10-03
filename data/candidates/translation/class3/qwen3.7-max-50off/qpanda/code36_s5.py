# EVAL_META: task_id=36, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CNOT, Qubit

def bv_function(s):
    n = len(s)
    qubits = [Qubit() for _ in range(n + 1)]
    qc = QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc << CNOT(qubits[index], qubits[n])
    return qc
