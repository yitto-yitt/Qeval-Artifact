# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit.circuit import ParameterExpression


def remove_unassigned_parameterized_gates(circuit):
    def _is_unassigned(param):
        return isinstance(param, ParameterExpression) and len(param.parameters) > 0

    kept_instructions = []
    for instruction in circuit.data:
        operation = instruction.operation
        if not any(_is_unassigned(param) for param in operation.params):
            kept_instructions.append(instruction)

    circuit.data.clear()
    for instruction in kept_instructions:
        circuit.append(instruction.operation, instruction.qubits, instruction.clbits)

    return circuit
