# EVAL_META: task_id=86, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, H, CNOT

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)


def _build_base():
    circ = QCircuit()
    circ << H(qubits[0])
    circ << CNOT(qubits[0], qubits[1])
    circ << CNOT(qubits[1], qubits[2])
    circ << CNOT(qubits[2], qubits[3])
    circ << CNOT(qubits[3], qubits[4])
    return circ


def _collect_linear_blocks(gate_ops, max_block_width=None):
    blocks = []
    current = []
    current_qubits = set()

    def is_linear(op):
        return op[0] in ("H_skip", "CNOT")

    for op in gate_ops:
        name, qs = op
        if name == "CNOT":
            new_qubits = current_qubits | set(qs)
            if max_block_width is not None and len(new_qubits) > max_block_width and current:
                blocks.append(current)
                current = []
                current_qubits = set()
                new_qubits = set(qs)
            current.append(op)
            current_qubits = new_qubits
        else:
            if current:
                blocks.append(current)
            current = []
            current_qubits = set()
    if current:
        blocks.append(current)
    return blocks


def collect_linear_blocks_with_and_without_limit():
    base_circ = _build_base()

    gate_ops = [
        ("H", [0]),
        ("CNOT", [0, 1]),
        ("CNOT", [1, 2]),
        ("CNOT", [2, 3]),
        ("CNOT", [3, 4]),
    ]

    linear_ops = gate_ops[1:]

    full_blocks = _collect_linear_blocks(linear_ops, max_block_width=None)
    limited_blocks = _collect_linear_blocks(linear_ops, max_block_width=3)

    full_result = {
        "circuit": base_circ,
        "linear_blocks": full_blocks,
        "num_blocks": len(full_blocks),
    }
    limited_result = {
        "circuit": base_circ,
        "linear_blocks": limited_blocks,
        "num_blocks": len(limited_blocks),
    }

    return full_result, limited_result


if __name__ == "__main__":
    full, limited = collect_linear_blocks_with_and_without_limit()
    print("Full blocks:", full["num_blocks"], full["linear_blocks"])
    print("Limited blocks:", limited["num_blocks"], limited["linear_blocks"])
    machine.finalize()
