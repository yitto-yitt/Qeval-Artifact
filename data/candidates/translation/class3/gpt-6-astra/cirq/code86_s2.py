# EVAL_META: task_id=86, framework=cirq, class=3
import cirq


def collect_linear_blocks_with_and_without_limit():
    qubits = cirq.LineQubit.range(5)
    circuit = cirq.Circuit(
        cirq.H(qubits[0]),
        *(cirq.CNOT(qubits[i], qubits[i + 1]) for i in range(4)),
    )

    def collect(max_block_width=None):
        result = cirq.Circuit()
        block = []
        block_qubits = set()

        def flush():
            if len(block) >= 2:
                result.append(
                    cirq.CircuitOperation(cirq.FrozenCircuit(block)),
                    strategy=cirq.InsertStrategy.NEW,
                )
            elif block:
                result.append(block[0], strategy=cirq.InsertStrategy.NEW)
            block.clear()
            block_qubits.clear()

        for operation in circuit.all_operations():
            if operation.gate not in (cirq.CNOT, cirq.SWAP):
                flush()
                result.append(operation, strategy=cirq.InsertStrategy.NEW)
                continue

            combined_qubits = block_qubits.union(operation.qubits)
            if (
                max_block_width is not None
                and len(combined_qubits) > max_block_width
            ):
                flush()

            block.append(operation)
            block_qubits.update(operation.qubits)

        flush()
        return result

    return collect(), collect(max_block_width=3)
