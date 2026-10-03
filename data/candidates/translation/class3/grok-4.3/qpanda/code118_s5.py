# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, C3SXGate

def create_c3sx_circuit():
    qc = QCircuit(4)
    c3sx_gate = C3SXGate()
    qc.append(c3sx_gate, [0, 1, 2, 3])
    return qc
