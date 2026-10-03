# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit.circuit import ParameterExpression

def remove_unassigned_parameterized_gates(circuit):
    def _has_unassigned_parameters(instruction):
        for param in getattr(instruction.operation, "params", []):
            if isinstance(param, ParameterExpression) and param.parameters:
                return True
        return False

    circuit.data = [
        instruction for instruction in circuit.data
        if not _has_unassigned_parameters(instruction)
    ]
    return circuit
