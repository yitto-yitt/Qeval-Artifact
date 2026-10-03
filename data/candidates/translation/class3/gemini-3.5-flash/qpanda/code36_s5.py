# EVAL_META: task_id=36, framework=qpanda, class=3
from pyqpanda3.core import qAllocMany, QCircuit, CNOT

def bv_function(s):
    n = len(s)
    qubits = qAllocMany(n + 1)
    circuit = QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit << CNOT(qubits[index], qubits[n])
    return circuit
