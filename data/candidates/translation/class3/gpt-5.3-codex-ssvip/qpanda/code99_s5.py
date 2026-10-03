# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import QCircuit

def remove_unassigned_parameterized_gates(circuit):
    if circuit is None:
        return QCircuit()

    try:
        instructions = list(circuit.data)
    except Exception:
        try:
            instructions = list(circuit)
        except Exception:
            return QCircuit()

    circuit_without_params = QCircuit()

    for instruction in instructions:
        op = None
        qargs = []
        cargs = []

        if isinstance(instruction, (tuple, list)):
            if len(instruction) >= 1:
                op = instruction[0]
            if len(instruction) >= 2:
                qargs = instruction[1]
            if len(instruction) >= 3:
                cargs = instruction[2]
        else:
            op = getattr(instruction, "operation", instruction)
            qargs = getattr(instruction, "qubits", [])
            cargs = getattr(instruction, "clbits", [])

        params = getattr(op, "params", None)
        has_unassigned = False
        if params is not None:
            if isinstance(params, (list, tuple)):
                if len(params) > 0:
                    p0 = params[0]
                    if hasattr(p0, "name") and not isinstance(p0, (int, float, complex)):
                        has_unassigned = True
            else:
                if hasattr(params, "name") and not isinstance(params, (int, float, complex)):
                    has_unassigned = True

        if not has_unassigned:
            try:
                circuit_without_params.insert(op)
            except Exception:
                try:
                    circuit_without_params << op
                except Exception:
                    pass

    return circuit_without_params
