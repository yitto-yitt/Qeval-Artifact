# EVAL_META: task_id=60, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, CNOT, S, SDG

def create_cy_gate():
    circuit = QCircuit()
    q = circuit.qAlloc(2)
    circuit << SDG(q[1]) << CNOT(q[0], q[1]) << S(q[1])
    return circuit
