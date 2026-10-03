# EVAL_META: task_id=5, framework=pennylane, class=2
import pennylane as qml


def create_state_prep():
    dev = qml.device('default.qubit', wires=2)
    
    @qml.qnode(dev)
    def circuit():
        qml.BasisState([0, 1], wires=[0, 1])
        return qml.state()
    
    # We need to return the operation that prepares the state, not the result of execution
    ops = [qml.BasisState([0, 1], wires=[0, 1])]
    return ops
