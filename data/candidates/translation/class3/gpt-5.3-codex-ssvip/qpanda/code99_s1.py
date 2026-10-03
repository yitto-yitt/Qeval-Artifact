# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import QCircuit

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = QCircuit()
    if not hasattr(circuit, "ops"):
        return new_circuit

    for op in circuit.ops:
        params = getattr(op, "params", None)
        has_unassigned = False

        if params is not None:
            if hasattr(params, "is_parameter") and params.is_parameter():
                has_unassigned = True
            elif isinstance(params, (list, tuple)) and len(params) > 0:
                p0 = params[0]
                if hasattr(p0, "is_parameter") and p0.is_parameter():
                    has_unassigned = True

        if not has_unassigned:
            new_circuit.insert(op)

    return new_circuit
