# EVAL_META: task_id=99, framework=qiskit, class=3
from qiskit.circuit import ParameterExpression


def remove_unassigned_parameterized_gates(circuit):
    new_circuit = circuit.copy_empty_like()

    for instruction in circuit.data:
        params = getattr(instruction.operation, "params", [])
        has_unassigned = False

        for param in params:
            if isinstance(param, ParameterExpression) and len(param.parameters) > 0:
                has_unassigned = True
                break

        if not has_unassigned:
            new_circuit.append(instruction.operation, instruction.qubits, instruction.clbits)

    return new_circuit
