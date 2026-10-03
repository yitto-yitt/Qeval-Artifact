# EVAL_META: task_id=60, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, S, Sdg, CX

def create_cy_gate():
    circuit = QCircuit(2)
    circuit.insert(Sdg(1))
    circuit.insert(CX(0, 1))
    circuit.insert(S(1))
    return circuit
