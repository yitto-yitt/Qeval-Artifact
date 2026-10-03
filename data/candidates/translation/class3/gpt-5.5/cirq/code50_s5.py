# EVAL_META: task_id=50, framework=cirq, class=3
import cirq

def remove_gate_in_position(circuit, position):
    operations = list(circuit.findall_operations(lambda op: True))
    if isinstance(position, slice):
        circuit.batch_remove(operations[position])
    else:
        circuit.batch_remove([operations[position]])
    return circuit
