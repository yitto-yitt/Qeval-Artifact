# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml

def rx_gate(value=None):
    if value is not None:
        with qml.tape.QuantumTape() as tape:
            qml.RX(value, wires=0)
        return tape
    
    def circuit(theta):
        qml.RX(theta, wires=0)
        
    return circuit
