# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QGate

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QCircuit()
    for op in circuit:
        if isinstance(op, QGate):
            params = op.parameters()
            has_unassigned = False
            for p in params:
                try:
                    float(p)
                except (TypeError, ValueError):
                    has_unassigned = True
                    break
            if has_unassigned:
                continue
        new_circuit << op
    return new_circuit
