# EVAL_META: task_id=26, framework=pennylane, class=3
import pennylane as qml
from pennylane import numpy as np


def bell_dag():
    dev = qml.device('default.qubit', wires=3)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.probs(wires=[0, 1, 2])
    
    tape = circuit.qtape
    
    # Create a DAG representation manually since PennyLane doesn't have direct DAG conversion
    # We'll represent the operations in a list which serves as our "DAG"
    ops_list = []
    for op in tape.operations:
        ops_list.append(op)
    
    return ops_list
