# EVAL_META: task_id=99, framework=qiskit, class=3

from qiskit.circuit import ParameterExpression

def remove_unassigned_parameterized_gates(circuit):
    circuit.data[:] = [
        instruction
        for instruction in circuit.data
        if not any(
            isinstance(p, ParameterExpression) and p.parameters
            for p in getattr(instruction.operation, "params", [])
        )
    ]
    return circuit
