# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg


def remove_unassigned_parameterized_gates(circuit):
    if isinstance(circuit, QProg):
        new_circuit = QProg()
    else:
        new_circuit = QCircuit()

    for node in circuit:
        keep = True
        try:
            params = node.parameters()
            if params is not None and len(params) > 0:
                for p in params:
                    if hasattr(p, "is_constant"):
                        if not p.is_constant():
                            keep = False
                            break
                    else:
                        try:
                            float(p)
                        except (TypeError, ValueError):
                            keep = False
                            break
        except Exception:
            keep = True

        if keep:
            new_circuit << node

    return new_circuit
