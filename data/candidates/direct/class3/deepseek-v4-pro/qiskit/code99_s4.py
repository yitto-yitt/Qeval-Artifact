# EVAL_META: task_id=99, framework=qiskit, class=3

def remove_unassigned_parameterized_gates(circuit):
    def _has_unassigned_parameters(params):
        for param in params:
            free_params = getattr(param, "parameters", None)
            if free_params is not None and len(free_params) > 0:
                return True
        return False

    kept = []
    for item in circuit.data:
        if hasattr(item, "operation"):
            operation = item.operation
        else:
            operation = item[0]

        if not _has_unassigned_parameters(operation.params):
            kept.append(item)

    circuit.data.clear()
    circuit.data.extend(kept)
    return circuit
