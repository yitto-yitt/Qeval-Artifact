# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml

def rx_gate(value=None):
    if value is None:
        theta = qml.numpy.array(0.0, requires_grad=True)
    else:
        theta = value
    quantum_circuit = qml.tape.QuantumScript([qml.RX(theta, wires=0)])
    return quantum_circuit
