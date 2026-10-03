# EVAL_META: task_id=99, framework=qiskit, class=3

def remove_unassigned_parameterized_gates(circuit):
    result = circuit.copy()
    result.data = [
        instruction
        for instruction in result.data
        if not instruction.operation.is_parameterized()
    ]
    return result
