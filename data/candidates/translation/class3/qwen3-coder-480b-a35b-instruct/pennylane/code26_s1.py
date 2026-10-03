# EVAL_META: task_id=26, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np


def bell_dag():
    dev = qml.device('default.qubit', wires=3)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.probs(wires=[0])
    
    tape = circuit.qtape
    
    # Create a DAG-like representation manually since PennyLane doesn't have direct DAG conversion
    # We'll return the tape which contains the operations in order
    return tape
