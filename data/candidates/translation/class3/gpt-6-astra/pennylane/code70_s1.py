# EVAL_META: task_id=70, framework=pennylane, class=3
import pennylane as qml
from math import pi

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    return qml.tape.QuantumScript(
        [
            qml.Hadamard(wires=0),
            qml.CSWAP(wires=[0, 1, 2]),
            qml.Hadamard(wires=1),
            qml.ControlledPhaseShift(-pi / 2, wires=[1, 0]),
        ]
    )
