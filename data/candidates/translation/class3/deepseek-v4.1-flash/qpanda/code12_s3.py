# EVAL_META: task_id=12, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT, get_unitary as qp_get_unitary

def get_unitary():
    circuit = QCircuit()
    circuit << H(0) << CNOT(0, 1)
    return qp_get_unitary(circuit)
