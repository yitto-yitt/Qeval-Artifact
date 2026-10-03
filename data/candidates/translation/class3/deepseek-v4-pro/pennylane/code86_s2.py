# EVAL_META: task_id=86, framework=pennylane, class=3
import pennylane as qml


def collect_linear_blocks_with_and_without_limit():
    base_ops = [
        qml.Hadamard(wires=0),
        qml.CNOT(wires=[0, 1]),
        qml.CNOT(wires=[1, 2]),
        qml.CNOT(wires=[2, 3]),
        qml.CNOT(wires=[3, 4]),
    ]

    def _collect_linear_blocks(ops, max_block_width=None):
        collected = []
        block_ops = []
        block_wires = set()

        for op in ops:
            if op.name == "CNOT":
                if (
                    max_block_width is not None
                    and block_ops
                    and len(block_wires | set(op.wires)) > max_block_width
                ):
                    wires = sorted(block_wires)
                    U = qml.matrix(qml.tape.QuantumTape(block_ops), wire_order=wires)
                    collected.append(qml.QubitUnitary(U, wires=wires))
                    block_ops = []
                    block_wires = set()

                block_ops.append(op)
                block_wires.update(op.wires)
            else:
                if block_ops:
                    wires = sorted(block_wires)
                    U = qml.matrix(qml.tape.QuantumTape(block_ops), wire_order=wires)
                    collected.append(qml.QubitUnitary(U, wires=wires))
                    block_ops = []
                    block_wires = set()
                collected.append(op)

        if block_ops:
            wires = sorted(block_wires)
            U = qml.matrix(qml.tape.QuantumTape(block_ops), wire_order=wires)
            collected.append(qml.QubitUnitary(U, wires=wires))

        return collected

    full_ops = _collect_linear_blocks(base_ops)
    limited_ops = _collect_linear_blocks(base_ops, max_block_width=3)

    return qml.tape.QuantumTape(full_ops), qml.tape.QuantumTape(limited_ops)
