# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg


def remove_unassigned_parameterized_gates(circuit):
    result = QCircuit()
    for op in circuit:
        params = op.parameters()
        has_unassigned = False
        for p in params:
            try:
                float(p)
            except (TypeError, ValueError):
                has_unassigned = True
                break
        if not has_unassigned:
            result << op
    return result
