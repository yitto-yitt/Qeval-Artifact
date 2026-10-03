# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit


def inv_circuit(n):
    qc = QuantumCircuit(n)
    for i in range(2):
        qc.h(i + 1)
    for i in range(2):
        qc.cnot(i + 1, i + 3)
    if hasattr(qc, "inverse"):
        return qc.inverse()
    return qc.dagger()
