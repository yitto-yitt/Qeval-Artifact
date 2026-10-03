# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml

def rx_gate(value=None):
    def circuit(theta):
        qml.RX(theta, wires=0)
    
    dev = qml.device('default.qubit', wires=1)
    
    if value is not None:
        @qml.qnode(dev)
        def bound_circuit():
            circuit(value)
            return qml.state()
        
        # Return the tape with the bound parameter
        with qml.tape.QuantumTape() as tape:
            qml.RX(value, wires=0)
        return tape
    else:
        # Return a function that can accept the parameter
        @qml.qnode(dev)
        def parametrized_circuit(theta):
            circuit(theta)
            return qml.state()
        
        return parametrized_circuit
