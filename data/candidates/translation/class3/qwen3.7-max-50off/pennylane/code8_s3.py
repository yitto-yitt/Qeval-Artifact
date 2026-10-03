# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml

def rx_gate(value=None):
    with qml.tape.QuantumTape() as tape:
        if value is not None:
            qml.RX(value, wires=0)
        else:
            qml.RX("theta", wires=0)
    return tape
