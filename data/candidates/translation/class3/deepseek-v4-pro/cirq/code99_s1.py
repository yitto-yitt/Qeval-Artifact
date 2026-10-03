# EVAL_META: task_id=99, framework=cirq, class=3
import cirq

def remove_unassigned_parameterized_gates(circuit):
    """Remove all gates with unassigned parameters from the circuit."""
    new_circuit = cirq.Circuit(
        op for op in circuit.all_operations()
        if not cirq.is_parameterized(op)
    )
    return new_circuit
