# EVAL_META: task_id=86, framework=cirq, class=3
import cirq

def collect_linear_blocks_with_and_without_limit():
    q = cirq.LineQubit.range(5)
    qc = cirq.Circuit(
        cirq.H(q[0]),
        cirq.CX(q[0], q[1]),
        cirq.CX(q[1], q[2]),
        cirq.CX(q[2], q[3]),
        cirq.CX(q[3], q[4]),
    )

    def _collect_linear_blocks(circuit, max_block_width=None):
        collected = cirq.Circuit()
        block_ops = []

        def flush():
            if block_ops:
                collected.append(
                    cirq.CircuitOperation(cirq.FrozenCircuit(*block_ops))
                )
                block_ops.clear()

        for op in circuit.all_operations():
            if isinstance(op.gate, cirq.CXGate):
                block_qubits = {qb for block_op in block_ops for qb in block_op.qubits}
                new_width = len(block_qubits | set(op.qubits))
                if max_block_width is not None and new_width > max_block_width:
                    flush()
                block_ops.append(op)
            else:
                flush()
                collected.append(op)

        flush()
        return collected

    full_block = _collect_linear_blocks(qc)
    limited_block = _collect_linear_blocks(qc, max_block_width=3)
    return full_block, limited_block
