# EVAL_META: task_id=99, framework=cirq, class=3
import cirq

def remove_unassigned_parameterized_gates(circuit):
    new_circuit = cirq.Circuit()
    for moment in circuit:
        for op in moment:
            if not cirq.is_parameterized(op):
                new_circuit.append(op)
    return new_circuit
