# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml
from pennylane.operation import Operator, AnyWires
from pennylane.tape import QuantumScript

class LinearBlock(Operator):
    num_wires = AnyWires
    
    def __init__(self, operators, wires, id=None):
        self.operators = operators
        super().__init__(wires=wires, id=id)

def collect_linear_blocks_with_and_without_limit():
    full_block = QuantumScript([
        qml.Hadamard(wires=0),
        LinearBlock([
            qml.CNOT(wires=[0, 1]),
            qml.CNOT(wires=[1, 2]),
            qml.CNOT(wires=[2, 3]),
            qml.CNOT(wires=[3, 4])
        ], wires=[0, 1, 2, 3, 4])
    ])
    
    limited_block = QuantumScript([
        qml.Hadamard(wires=0),
        LinearBlock([
            qml.CNOT(wires=[0, 1]),
            qml.CNOT(wires=[1, 2])
        ], wires=[0, 1, 2]),
        LinearBlock([
            qml.CNOT(wires=[2, 3]),
            qml.CNOT(wires=[3, 4])
        ], wires=[2, 3, 4])
    ])
    
    return full_block, limited_block
