# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import init, qalloc, QCircuit, X, RY, CNOT

try:
    from pyqpanda3.core import CRY
except ImportError:
    try:
        from pyqpanda3.core import CR as CRY
    except ImportError:
        CRY = None

def tensor_circuits():
    init()
    q = qalloc(3)
    circuit = QCircuit()

    if CRY is not None:
        circuit << CRY(q[0], q[1], 0.2)
    else:
        circuit << RY(q[1], 0.1)
        circuit << CNOT(q[0], q[1])
        circuit << RY(q[1], -0.1)
        circuit << CNOT(q[0], q[1])

    circuit << X(q[2])
    return circuit
