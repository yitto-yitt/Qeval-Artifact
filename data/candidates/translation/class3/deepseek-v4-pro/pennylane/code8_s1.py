# EVAL_META: task_id=8, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np

def rx_gate(value=None):
    if value is None:
        theta = np.array(0., requires_grad=True)
        ops = [qml.RX(theta, wires=0)]
    else:
        ops = [qml.RX(value, wires=0)]
    return qml.tape.QuantumScript(ops, [])
