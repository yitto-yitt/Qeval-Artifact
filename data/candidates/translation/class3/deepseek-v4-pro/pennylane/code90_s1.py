# EVAL_META: task_id=90, framework=pennylane, class=3
import pennylane as qml

def create_custom_controlled():
    dev = qml.device('default.qubit', wires=4)

    @qml.qnode(dev)
    def circuit():
        # Custom 2-qubit operation: X on first target, H on second target
        def custom_op(w):
            qml.X(wires=w[0])
            qml.H(wires=w[1])

        # Apply controlled version with 2 control qubits (0 and 3) onto targets (1 and 2)
        qml.ctrl(custom_op, control=[0, 3])(w=[1, 2])
        return qml.state()

    return circuit
