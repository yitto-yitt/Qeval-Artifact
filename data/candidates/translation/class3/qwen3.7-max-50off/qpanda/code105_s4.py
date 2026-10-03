# EVAL_META: task_id=105, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QuantumMachine

def initialize_cnot_dihedral():
    machine = QuantumMachine()
    q = machine.qAlloc_many(2)
    circ = QCircuit()
    circ.cnot(q[0], q[1])
    circ.t(q[0])
    return circ
