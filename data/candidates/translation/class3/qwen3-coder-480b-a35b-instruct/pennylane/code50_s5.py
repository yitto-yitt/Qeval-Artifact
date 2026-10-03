# EVAL_META: task_id=50, framework=pennylane, class=3
import pennylane as qml

def remove_gate_in_position(circuit, position):
    new_tape = circuit.copy()
    ops = list(new_tape.operations)
    ops.pop(position)
    new_tape = type(new_tape)(ops + new_tape.measurements, shots=new_tape.shots)
    return new_tape
