# EVAL_META: task_id=57, framework=pennylane, class=3
import pennylane as qml

def create_swap_gate():
    def swap_template(wires):
        qml.CNOT(wires=[wires[0], wires[1]])
        qml.CNOT(wires=[wires[1], wires[0]])
        qml.CNOT(wires=[wires[0], wires[1]])
    return swap_template
