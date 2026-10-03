# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml

def collect_linear_blocks_with_and_without_limit():
    with qml.tape.QuantumTape() as full_block:
        qml.Hadamard(wires=0)
        qml.prod(
            qml.CNOT(wires=[0, 1]),
            qml.CNOT(wires=[1, 2]),
            qml.CNOT(wires=[2, 3]),
            qml.CNOT(wires=[3, 4])
        )
        
    with qml.tape.QuantumTape() as limited_block:
        qml.Hadamard(wires=0)
        qml.prod(
            qml.CNOT(wires=[0, 1]),
            qml.CNOT(wires=[1, 2])
        )
        qml.prod(
            qml.CNOT(wires=[2, 3]),
            qml.CNOT(wires=[3, 4])
        )
        
    return full_block, limited_block
