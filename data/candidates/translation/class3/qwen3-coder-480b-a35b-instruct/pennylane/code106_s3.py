# EVAL_META: task_id=106, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np


def compose_cnot_dihedral():
    # Create first circuit
    def circuit1():
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)
    
    # Create second circuit (same as first but with additional X gate on qubit 1)
    def circuit2():
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)
        qml.X(wires=1)
    
    # Convert to operations and create dihedral elements
    ops1 = qml.transforms.decompose_circuit(circuit1)()
    ops2 = qml.transforms.decompose_circuit(circuit2)()
    
    # Since PennyLane doesn't have direct CNOTDihedral support, we need to work around this
    # We'll create a combined circuit that represents the composition
    def composed_circuit():
        # Apply circuit2 first (as per composition order), then circuit1
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)
        qml.X(wires=1)
        qml.CNOT(wires=[0, 1])
        qml.T(wires=0)
    
    # Return the decomposed operations representing the composed element
    return qml.transforms.decompose_circuit(composed_circuit)()
