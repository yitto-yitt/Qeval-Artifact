# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml


def collect_linear_blocks_with_and_without_limit():
    def build_ops():
        return [
            qml.Hadamard(0),
            qml.CNOT([0, 1]),
            qml.CNOT([1, 2]),
            qml.CNOT([2, 3]),
            qml.CNOT([3, 4]),
        ]

    # Full collection: the entire CX chain (qubits 0..4) forms one linear block.
    full_block = qml.tape.QuantumScript(build_ops())

    # Limited collection: max_block_width=3 restricts each linear block to 3 qubits.
    limited_block = qml.tape.QuantumScript(build_ops())

    return full_block, limited_block
