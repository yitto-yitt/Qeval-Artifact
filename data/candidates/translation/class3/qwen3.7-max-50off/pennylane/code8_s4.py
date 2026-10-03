# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml

def rx_gate(value=None):
    with qml.tape.QuantumTape() as tape:
        qml.RX(value if value is not None else "theta", wires=0)
    return tape
