# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml

def rx_gate(value=None):
    def circuit():
        if value is not None:
            qml.RX(value, wires=0)
        else:
            # In PennyLane, we can't create a parameterized gate without specifying a value
            # We'll return a template that expects a parameter
            pass
    
    if value is not None:
        dev = qml.device('default.qubit', wires=1)
        @qml.qnode(dev)
        def bound_circuit():
            qml.RX(value, wires=0)
            return qml.state()
        
        # Return the operation itself when value is provided
        return qml.RX(value, wires=0)
    else:
        # Return a function that creates the parameterized operation
        return lambda theta: qml.RX(theta, wires=0)
