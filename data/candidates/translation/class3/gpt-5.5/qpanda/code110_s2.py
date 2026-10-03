# EVAL_META: task_id=110, framework=qpanda, class=3
from pyqpanda3.core import *
import copy

def equivalent_clifford_circuit(circuit, n):
    qc_list = []
    for _ in range(n):
        try:
            qc_list.append(copy.deepcopy(circuit))
        except Exception:
            qc_list.append(circuit)
    return qc_list
