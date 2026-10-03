# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml
from pennylane import QuantumTape

def collect_linear_blocks_with_and_without_limit():
    qc = QuantumTape()
    with qc:
        qml.Hadamard(0)
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        qml.CNOT(wires=[2, 3])
        qml.CNOT(wires=[3, 4])
    pm_full = qc
    full_block = pm_full
    pm_limited = QuantumTape()
    with pm_limited:
        qml.Hadamard(0)
        qml.CNOT(wires=[0, 1])
        qml.CNOT(wires=[1, 2])
        qml.CNOT(wires=[2, 3])
        qml.CNOT(wires=[3, 4])
    limited_block = pm_limited
    return full_block, limited_block
