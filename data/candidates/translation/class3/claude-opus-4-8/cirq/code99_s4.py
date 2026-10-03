# EVAL_META: task_id=99, framework=cirq, class=3
import cirq
import sympy


def remove_unassigned_parameterized_gates(circuit):
    new_ops = []
    for op in circuit.all_operations():
        if not cirq.is_parameterized(op):
            new_ops.append(op)
    return cirq.Circuit(new_ops)
