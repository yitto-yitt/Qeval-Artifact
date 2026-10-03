# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml


def collect_linear_blocks_with_and_without_limit():
    chain = [qml.CNOT(wires=[i, i + 1]) for i in range(4)]

    def collect(max_block_width):
        operations = [qml.Hadamard(wires=0)]
        block = []
        block_wires = []

        def append_block():
            if not block:
                return
            matrix = qml.matrix(
                qml.tape.QuantumScript(block),
                wire_order=block_wires,
            )
            operations.append(qml.QubitUnitary(matrix, wires=block_wires))

        for gate in chain:
            candidate_wires = list(dict.fromkeys(block_wires + list(gate.wires)))
            if max_block_width is not None and len(candidate_wires) > max_block_width:
                append_block()
                block = []
                block_wires = []
                candidate_wires = list(gate.wires)
            block.append(gate)
            block_wires = candidate_wires

        append_block()
        return qml.tape.QuantumScript(operations)

    return collect(None), collect(3)
