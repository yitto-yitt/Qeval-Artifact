# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda3 import QuantumCircuit

def create_c3sx_circuit():
    qc = QuantumCircuit(4)
    qc.c3sx(0, 1, 2, 3)
    return qc
