# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml
import numpy as np

class LinearFunction(qml.operation.Operation):
    num_wires = qml.operation.AnyWires
    
    def __init__(self, matrix, wires, id=None):
        self._matrix = np.array(matrix)
        super().__init__(wires=wires, id=id)
        
    def matrix(self, wire_order=None):
        if wire_order is None or list(wire_order) == list(self.wires):
            return self._matrix
        return qml.operation.expand_matrix(self._matrix, self.wires, wire_order)

def collect_linear_blocks_with_and_without_limit():
    ops_full = [
        qml.CNOT(wires=[0, 1]),
        qml.CNOT(wires=[1, 2]),
        qml.CNOT(wires=[2, 3]),
        qml.CNOT(wires=[3, 4])
    ]
    mat_full = qml.matrix(qml.tape.QuantumTape(ops_full), wire_order=[0, 1, 2, 3, 4])
    
    ops_lim1 = [
        qml.CNOT(wires=[0, 1]),
        qml.CNOT(wires=[1, 2])
    ]
    mat_lim1 = qml.matrix(qml.tape.QuantumTape(ops_lim1), wire_order=[0, 1, 2])
    
    ops_lim2 = [
        qml.CNOT(wires=[2, 3]),
        qml.CNOT(wires=[3, 4])
    ]
    mat_lim2 = qml.matrix(qml.tape.QuantumTape(ops_lim2), wire_order=[2, 3, 4])
    
    full_tape = qml.tape.QuantumTape([
        qml.Hadamard(wires=0),
        LinearFunction(mat_full, wires=[0, 1, 2, 3, 4])
    ])
    
    limited_tape = qml.tape.QuantumTape([
        qml.Hadamard(wires=0),
        LinearFunction(mat_lim1, wires=[0, 1, 2]),
        LinearFunction(mat_lim2, wires=[2, 3, 4])
    ])
    
    return full_tape, limited_tape
