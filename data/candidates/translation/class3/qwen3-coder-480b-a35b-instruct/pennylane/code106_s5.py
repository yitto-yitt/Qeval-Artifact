# EVAL_META: task_id=106, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np


def compose_cnot_dihedral():
    # Create first circuit
    def circuit1():
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)
    
    # Create second circuit (same as first + X gate on qubit 1)
    def circuit2():
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)
        qml.PauliX(wires=1)
    
    # In PennyLane, we work with operations directly rather than converting to specific classes
    # Since there's no direct CNOTDihedral equivalent in PennyLane 0.45.1,
    # we return the operations that represent the composed circuit
    ops1 = [qml.CNOT(wires=[0, 1]), qml.T(wires=0)]
    ops2 = [qml.CNOT(wires=[0, 1]), qml.T(wires=0), qml.PauliX(wires=1)]
    
    # Compose by combining operations
    composed_ops = ops1 + ops2
    
    return composed_ops
