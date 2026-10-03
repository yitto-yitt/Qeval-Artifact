# EVAL_META: task_id=118, framework=qpanda, class=3
import math
from pyqpanda3.core import QuantumCircuit

def create_c3sx_circuit():
    qc = QuantumCircuit(4)
    qc.h(3)
    qc.mcp([0, 1, 2], 3, math.pi / 2)
    qc.h(3)
    return qc
