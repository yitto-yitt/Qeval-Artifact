# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit.circuit import ParameterExpression


def remove_unassigned_parameterized_gates(circuit):
    result = circuit.copy_empty_like()
    for instruction in circuit.data:
        if any(
            isinstance(param, ParameterExpression) and param.parameters
            for param in instruction.operation.params
        ):
            continue
        result.append(
            instruction.operation, instruction.qubits, instruction.clbits
        )
    return result
