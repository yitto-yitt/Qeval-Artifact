# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml


def _build_ops():
    return [
        qml.Hadamard(wires=0),
        qml.CNOT(wires=[0, 1]),
        qml.CNOT(wires=[1, 2]),
        qml.CNOT(wires=[2, 3]),
        qml.CNOT(wires=[3, 4]),
    ]


def _collect_linear_blocks(ops, max_block_width=None):
    """Group consecutive linear (CNOT/SWAP) gates into blocks.

    Returns a list where linear runs are collapsed into a single
    matrix-based operation (analog of a LinearFunction), respecting an
    optional maximum block width.
    """
    linear_types = (qml.CNOT, qml.SWAP)
    collected = []
    current = []
    current_wires = set()

    def flush():
        if not current:
            return
        wires = sorted(current_wires)
        if len(current) == 1:
            collected.append(current[0])
        else:
            mat = qml.matrix(qml.tape.QuantumScript(list(current)), wire_order=wires)
            collected.append(qml.QubitUnitary(mat, wires=wires))

    for op in ops:
        if isinstance(op, linear_types):
            new_wires = current_wires.union(set(op.wires))
            if max_block_width is not None and len(new_wires) > max_block_width:
                flush()
                current[:] = []
                current_wires.clear()
                new_wires = set(op.wires)
            current.append(op)
            current_wires.update(op.wires)
        else:
            flush()
            current[:] = []
            current_wires.clear()
            collected.append(op)
    flush()
    return collected


def collect_linear_blocks_with_and_without_limit():
    full_ops = _collect_linear_blocks(_build_ops(), max_block_width=None)
    limited_ops = _collect_linear_blocks(_build_ops(), max_block_width=3)

    full_block = qml.tape.QuantumScript(full_ops)
    limited_block = qml.tape.QuantumScript(limited_ops)
    return full_block, limited_block
