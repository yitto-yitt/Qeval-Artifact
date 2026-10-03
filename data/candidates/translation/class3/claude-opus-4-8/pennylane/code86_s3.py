# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml
from pennylane.tape import QuantumScript


def collect_linear_blocks_with_and_without_limit():
    base_ops = [
        qml.Hadamard(wires=0),
        qml.CNOT(wires=[0, 1]),
        qml.CNOT(wires=[1, 2]),
        qml.CNOT(wires=[2, 3]),
        qml.CNOT(wires=[3, 4]),
    ]

    def collect_linear(ops, max_block_width=None):
        result = []
        block = []
        block_wires = set()

        def flush():
            if not block:
                return
            wires = sorted(block_wires)
            mat = qml.matrix(
                QuantumScript(list(block)), wire_order=wires
            )
            result.append(qml.QubitUnitary(mat, wires=wires))

        for op in ops:
            is_linear = op.name in ("CNOT", "SWAP")
            if not is_linear:
                flush()
                block = []
                block_wires = set()
                result.append(op)
                continue

            new_wires = block_wires | set(op.wires)
            if max_block_width is not None and len(new_wires) > max_block_width:
                flush()
                block = [op]
                block_wires = set(op.wires)
            else:
                block.append(op)
                block_wires = new_wires

        flush()
        return QuantumScript(result)

    full_block = collect_linear(base_ops, max_block_width=None)
    limited_block = collect_linear(base_ops, max_block_width=3)
    return full_block, limited_block
