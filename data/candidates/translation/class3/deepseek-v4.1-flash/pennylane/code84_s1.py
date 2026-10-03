# EVAL_META: task_id=84, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def controlled_custom_unitary_circuit():
    theta = 0.3
    phi = 0.2
    lam = 0.1
    U = np.array([
        [np.cos(theta/2), -np.exp(1j*lam)*np.sin(theta/2)],
        [np.exp(1j*phi)*np.sin(theta/2), np.exp(1j*(phi+lam))*np.cos(theta/2)]
    ])
    with qml.tape.QuantumTape() as tape:
        qml.ctrl(qml.QubitUnitary, control=0)(U, wires=1)
    return tape
