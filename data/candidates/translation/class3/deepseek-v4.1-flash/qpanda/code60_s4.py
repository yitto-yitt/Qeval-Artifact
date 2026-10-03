# EVAL_META: task_id=60, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, qAlloc, SDG, CNOT, S

def create_cy_gate():
    q = qAlloc(2)
    circuit = QCircuit()
    circuit << SDG(q[1])
    circuit << CNOT(q[0], q[1])
    circuit << S(q[1])
    return circuit
