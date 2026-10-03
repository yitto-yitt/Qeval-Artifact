# EVAL_META: task_id=50, framework=cirq, class=3
import cirq

def remove_gate_in_position(circuit, position):
    locations = [
        (moment_index, operation_index)
        for moment_index, moment in enumerate(circuit)
        for operation_index in range(len(moment.operations))
    ]
    moment_index, operation_index = locations[position]
    operations = list(circuit[moment_index].operations)
    del operations[operation_index]
    circuit[moment_index] = cirq.Moment(operations)
    return circuit
