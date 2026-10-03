# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml

class LinearFunction(qml.operation.Operation):
    num_wires = qml.operation.AnyWires
    
    def __init__(self, original_ops, wires, id=None):
        self.original_ops = original_ops
        super().__init__(wires=wires, id=id)
        
    def decomposition(self):
        return self.original_ops

def collect_linear_blocks_with_and_without_limit():
    # Full block tape (no block width restriction)
    ops_full = [
        qml.Hadamard(wires=0),
        LinearFunction(
            [
                qml.CNOT(wires=[0, 1]),
                qml.CNOT(wires=[1, 2]),
                qml.CNOT(wires=[2, 3]),
                qml.CNOT(wires=[3, 4])
            ],
            wires=[0, 1, 2, 3, 4]
        )
    ]
    full_tape = qml.tape.QuantumTape(ops_full)
    
    # Limited block tape (max_block_width of 3)
    ops_lim = [
        qml.Hadamard(wires=0),
        LinearFunction(
            [
                qml.CNOT(wires=[0, 1]),
                qml.CNOT(wires=[1, 2])
            ],
            wires=[0, 1, 2]
        ),
        LinearFunction(
            [
                qml.CNOT(wires=[2, 3]),
                qml.CNOT(wires=[3, 4])
            ],
            wires=[2, 3, 4]
        )
    ]
    limited_tape = qml.tape.QuantumTape(ops_lim)
    
    return full_tape, limited_tape
