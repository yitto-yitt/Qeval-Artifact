# EVAL_META: task_id=50, framework=pennylane, class=3
import pennylane as qml


def remove_gate_in_position(circuit, position):
    ops = list(circuit.operations)
    del ops[position]
    measurements = list(circuit.measurements)
    new_circuit = qml.tape.QuantumScript(ops, measurements, shots=circuit.shots)
    return new_circuit
