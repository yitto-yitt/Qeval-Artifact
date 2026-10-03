# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml


def collect_linear_blocks_with_and_without_limit():
    chain = [qml.CNOT(wires=[i, i + 1]) for i in range(4)]

    def collect(max_block_width=None):
        operations = [qml.Hadamard(wires=0)]
        block = []
        block_wires = set()

        def append_block(gates, wires):
            if len(gates) == 1:
                operations.append(gates[0])
            elif gates:
                wire_order = sorted(wires)
                matrix = qml.matrix(
                    qml.tape.QuantumScript(gates),
                    wire_order=wire_order,
                )
                operations.append(
                    qml.QubitUnitary(matrix, wires=wire_order)
                )

        for gate in chain:
            combined_wires = block_wires | set(gate.wires)
            if (
                max_block_width is not None
                and len(combined_wires) > max_block_width
            ):
                append_block(block, block_wires)
                block = []
                block_wires = set()

            block.append(gate)
            block_wires.update(gate.wires)

        append_block(block, block_wires)
        return qml.tape.QuantumScript(operations)

    return collect(), collect(max_block_width=3)
