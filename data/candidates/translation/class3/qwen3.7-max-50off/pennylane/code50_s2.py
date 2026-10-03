# EVAL_META: task_id=50, framework=pennylane, class=3
import pennylane as qml

def remove_gate_in_position(circuit, position):
    if isinstance(circuit, qml.tape.QuantumScript):
        ops = list(circuit.operations)
        del ops[position]
        return qml.tape.QuantumScript(ops, circuit.measurements)
    elif isinstance(circuit, list):
        del circuit[position]
        return circuit
    else:
        del circuit[position]
        return circuit
