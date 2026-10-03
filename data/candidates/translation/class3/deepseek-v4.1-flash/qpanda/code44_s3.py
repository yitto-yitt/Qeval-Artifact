# EVAL_META: task_id=44, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, X, CRY


def tensor_circuits():
    # 2-qubit CRY circuit (control = qubit 0, target = qubit 1, angle = 0.2)
    bottom = QCircuit()
    bottom << CRY(0, 1, 0.2)

    # 1-qubit X circuit
    top = QCircuit()
    top << X(0)

    # Tensor product placing the 2-qubit CRY circuit first, then the 1-qubit X circuit
    result = QCircuit()
    result << CRY(0, 1, 0.2)
    result << X(2)

    return result
