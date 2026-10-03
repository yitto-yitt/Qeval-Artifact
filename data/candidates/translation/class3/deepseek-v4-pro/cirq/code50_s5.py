# EVAL_META: task_id=50, framework=cirq, class=3
import cirq

def remove_gate_in_position(circuit, position):
    cirq_circuit = circuit.copy()
    moment_index = position[0]
    qubit = position[1]
    moment = cirq_circuit[moment_index]
    new_moment = moment.without_operations_touching({qubit})
    del cirq_circuit[moment_index]
    cirq_circuit.insert(moment_index, new_moment)
    return cirq_circuit
