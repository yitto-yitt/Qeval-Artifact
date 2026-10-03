# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg


def remove_unassigned_parameterized_gates(circuit):
    if isinstance(circuit, QProg):
        source = circuit
        result = QProg()
    else:
        source = circuit
        result = QCircuit()

    for node in source:
        params = node.parameters()
        has_unassigned = False
        for p in params:
            try:
                float(p)
            except (TypeError, ValueError):
                has_unassigned = True
                break
        if not has_unassigned:
            result << node

    return result
