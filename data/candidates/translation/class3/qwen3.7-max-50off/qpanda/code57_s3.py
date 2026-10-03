# EVAL_META: task_id=57, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QuantumMachine, CNOT

def create_swap_gate():
    qm = QuantumMachine()
    q = qm.qAlloc_many(2)
    circ = QCircuit()
    circ << CNOT(q[0], q[1])
    circ << CNOT(q[1], q[0])
    circ << CNOT(q[0], q[1])
    return circ
