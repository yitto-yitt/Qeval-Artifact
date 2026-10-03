# EVAL_META: task_id=2, framework=qpanda, class=2
from pyqpanda3.core import QMachine, QCircuit, H, CNOT

def create_bell_statevector():
    qm = QMachine()
    q = qm.qAlloc(2)
    circ = QCircuit()
    circ << H(q[0]) << CNOT(q[0], q[1])
    qm.apply_circuit(circ)
    return qm.get_state()
