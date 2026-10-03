# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, QGate


def remove_unassigned_parameterized_gates(circuit):
    if isinstance(circuit, QProg):
        new_circuit = QProg()
    else:
        new_circuit = QCircuit()

    for node in circuit:
        try:
            gate = QGate(node)
        except Exception:
            new_circuit << node
            continue

        has_unassigned = False
        try:
            params = gate.parameters()
            for p in params:
                if p is None:
                    has_unassigned = True
                    break
                try:
                    float(p)
                except (TypeError, ValueError):
                    has_unassigned = True
                    break
        except Exception:
            has_unassigned = False

        if not has_unassigned:
            new_circuit << gate

    return new_circuit
