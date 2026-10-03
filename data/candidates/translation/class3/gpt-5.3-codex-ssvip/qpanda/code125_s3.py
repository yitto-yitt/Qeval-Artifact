# EVAL_META: task_id=125, framework=qpanda, class=3
from pyqpanda3.core import QProg, QCircuit, QGate


def circ_to_gate(circ):
    if isinstance(circ, QGate):
        return circ
    if isinstance(circ, QCircuit):
        return circ
    if isinstance(circ, QProg):
        qc = QCircuit()
        qc << circ
        return qc
    qc = QCircuit()
    qc << circ
    return qc
