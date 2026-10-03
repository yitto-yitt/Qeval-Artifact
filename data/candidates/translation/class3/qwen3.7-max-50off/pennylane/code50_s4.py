# EVAL_META: task_id=50, framework=pennylane, class=3
import pennylane as qml

def remove_gate_in_position(circuit, position):
    if hasattr(circuit, "operations"):
        ops = list(circuit.operations)
        del ops[position]
        return qml.tape.QuantumTape(ops, circuit.measurements)
    else:
        del circuit[position]
        return circuit
