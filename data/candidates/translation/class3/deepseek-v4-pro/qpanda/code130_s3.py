# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def inv_circuit(n):
    qc = QuantumCircuit(n)
    qc.cnot(2, 4)
    qc.cnot(1, 3)
    qc.h(2)
    qc.h(1)
    return qc
