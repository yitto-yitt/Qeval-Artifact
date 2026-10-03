# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit.circuit import ParameterExpression


def remove_unassigned_parameterized_gates(circuit):
    result = circuit.copy()
    result.data = [
        instruction
        for instruction in result.data
        if not any(
            isinstance(parameter, ParameterExpression) and parameter.parameters
            for parameter in instruction.operation.params
        )
    ]
    return result
