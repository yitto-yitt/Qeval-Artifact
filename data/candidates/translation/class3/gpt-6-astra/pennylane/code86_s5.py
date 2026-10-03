# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml


def collect_linear_blocks_with_and_without_limit():
    source = qml.tape.QuantumScript(
        [qml.Hadamard(wires=0)]
        + [qml.CNOT(wires=[i, i + 1]) for i in range(4)]
    )

    def collect(max_block_width=None):
        operations = []
        block = []
        block_wires = []

        def flush():
            if len(block) >= 2:
                matrix = qml.matrix(
                    qml.tape.QuantumScript(block),
                    wire_order=block_wires,
                )
                operations.append(qml.QubitUnitary(matrix, wires=block_wires))
            else:
                operations.extend(block)
            block.clear()
            block_wires.clear()

        for operation in source.operations:
            if not isinstance(operation, qml.CNOT):
                flush()
                operations.append(operation)
                continue

            combined_wires = list(
                dict.fromkeys(block_wires + list(operation.wires))
            )
            if (
                max_block_width is not None
                and len(combined_wires) > max_block_width
            ):
                flush()
                combined_wires = list(operation.wires)

            block.append(operation)
            block_wires[:] = combined_wires

        flush()
        return qml.tape.QuantumScript(operations)

    return collect(), collect(max_block_width=3)
