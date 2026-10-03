# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml

def rx_gate(value=None):
    if value is not None:
        dev = qml.device('default.qubit', wires=1)
        
        @qml.qnode(dev)
        def circuit():
            qml.RX(value, wires=0)
            return qml.state()
        
        # Return the tape containing the operation
        circuit()
        return circuit.qtape.operations[0]
    else:
        # In PennyLane, we typically work with templates or functions that take parameters directly
        # We'll return a function that can be called with the parameter
        def parametrized_rx(theta):
            qml.RX(theta, wires=0)
        return parametrized_rx
