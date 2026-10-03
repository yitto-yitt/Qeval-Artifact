# EVAL_META: task_id=5, framework=pennylane, class=2
import pennylane as qml


def create_state_prep():
    dev = qml.device('default.qubit', wires=2)
    
    @qml.qnode(dev)
    def circuit():
        qml.QubitStateVector([0, 1, 0, 0], wires=[0, 1])
        return qml.state()
    
    # We need to return the operation that prepares the state, not the result of execution
    ops = [qml.QubitStateVector([0, 1, 0, 0], wires=[0, 1])]
    return ops[0] if len(ops) == 1 else ops


def create_state_prep():
    return qml.QubitStateVector([0, 1, 0, 0], wires=[0, 1])
