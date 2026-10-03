# EVAL_META: task_id=99, framework=qiskit, class=3

from qiskit.circuit import ParameterExpression


def _gate_has_unassigned_parameters(operation):
    if hasattr(operation, "is_parameterized"):
        return operation.is_parameterized()

    params = getattr(operation, "params", [])
    return any(
        isinstance(param, ParameterExpression) and len(param.parameters) > 0
        for param in params
    )


def remove_unassigned_parameterized_gates(circuit):
    cleaned = circuit.copy_empty_like()

    qubit_indices = {qubit: idx for idx, qubit in enumerate(circuit.qubits)}
    clbit_indices = {clbit: idx for idx, clbit in enumerate(circuit.clbits)}

    for instruction in circuit.data:
        operation = instruction.operation

        if _gate_has_unassigned_parameters(operation):
            continue

        qargs = [cleaned.qubits[qubit_indices[q]] for q in instruction.qubits]
        cargs = [cleaned.clbits[clbit_indices[c]] for c in instruction.clbits]
        cleaned.append(operation, qargs, cargs)

    return cleaned
