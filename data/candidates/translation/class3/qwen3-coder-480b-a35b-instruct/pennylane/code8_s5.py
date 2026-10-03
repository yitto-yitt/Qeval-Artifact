# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml

def rx_gate(value=None):
    if value is not None:
        @qml.qnode(qml.device('default.qubit', wires=1))
        def circuit():
            qml.RX(value, wires=0)
            return qml.state()
        # Return the operation directly since we need to return the gate
        return qml.RX(value, wires=0)
    else:
        # For parameterized case, we create a function that accepts the parameter
        def parametrized_circuit(theta):
            qml.RX(theta, wires=0)
        return parametrized_circuit
