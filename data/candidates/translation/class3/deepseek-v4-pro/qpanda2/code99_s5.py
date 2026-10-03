# EVAL_META: task_id=99, framework=qpanda2, class=3
from pyqpanda import *
import numbers
import numpy as np

init(QMachineType.CPU)
_global_qubits = qAlloc_many(1)


def _is_unassigned_parameterized_gate(node):
    if not isinstance(node, QGate):
        return False

    params = None
    if hasattr(node, 'get_parameter'):
        try:
            params = node.get_parameter()
        except Exception:
            pass

    if params is None and hasattr(node, 'getParameter'):
        try:
            params = node.getParameter()
        except Exception:
            pass

    if params is None:
        return False

    if isinstance(params, (list, tuple, np.ndarray)):
        return any(not isinstance(p, (numbers.Number, np.number)) for p in params)

    return not isinstance(params, (numbers.Number, np.number))


def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QCircuit()
    for node in circuit:
        if _is_unassigned_parameterized_gate(node):
            continue
        new_circuit << node
    return new_circuit


finalize()
