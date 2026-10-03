# EVAL_META: task_id=145, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumTape

def qft_inverse(n):
    with QuantumTape() as tape:
        qml.adjoint(qml.QFT)(wires=list(range(n)))
    return tape
