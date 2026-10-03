# EVAL_META: task_id=60, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, qAlloc_many, Sdg, S, CNOT

def create_cy_gate():
    circuit = QCircuit()
    q = qAlloc_many(2)
    circuit << Sdg(q[1]) << CNOT(q[0], q[1]) << S(q[1])
    return circuit
