# EVAL_META: task_id=99, framework=qiskit, class=3

def _has_unassigned_parameters(operation):
    parameters = getattr(operation, "parameters", None)
    if parameters is not None:
        return bool(parameters)
    for parameter in getattr(operation, "params", ()):
        if getattr(parameter, "parameters", None):
            return True
    return False


def remove_unassigned_parameterized_gates(circuit):
    kept = [
        instruction
        for instruction in circuit.data
        if not _has_unassigned_parameters(instruction.operation)
    ]
    try:
        circuit.data = kept
    except AttributeError:
        circuit.data[:] = kept
    return circuit
