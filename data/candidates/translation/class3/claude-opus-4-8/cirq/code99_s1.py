# EVAL_META: task_id=99, framework=cirq, class=3
import cirq
import sympy


def _has_unassigned_param(op):
    for val in cirq.parameter_symbols(op):
        return True
    return False


def remove_unassigned_parameterized_gates(circuit):
    new_circuit = cirq.Circuit()
    for moment in circuit:
        kept_ops = [op for op in moment.operations if not cirq.is_parameterized(op)]
        if kept_ops:
            new_circuit.append(cirq.Moment(kept_ops))
    return new_circuit
