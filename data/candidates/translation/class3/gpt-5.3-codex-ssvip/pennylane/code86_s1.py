# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml

def collect_linear_blocks_with_and_without_limit():
    qc_ops = [
        qml.Hadamard(wires=0),
        qml.CNOT(wires=[0, 1]),
        qml.CNOT(wires=[1, 2]),
        qml.CNOT(wires=[2, 3]),
        qml.CNOT(wires=[3, 4]),
    ]

    full_block = qml.tape.QuantumScript(operations=list(qc_ops), measurements=[])
    limited_block = qml.tape.QuantumScript(operations=list(qc_ops), measurements=[])

    return full_block, limited_block
