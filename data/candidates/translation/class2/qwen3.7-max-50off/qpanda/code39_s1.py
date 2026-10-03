# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import QuantumCircuit, H, StateVector

def create_uniform_superposition(n):
    qc = QuantumCircuit(n)
    for i in range(n):
        qc << H(i)
    return StateVector(qc)
