# EVAL_META: task_id=86, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, QProg, H, CNOT

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)


def _build_circuit():
    circ = QCircuit()
    circ << H(qubits[0])
    circ << CNOT(qubits[0], qubits[1])
    circ << CNOT(qubits[1], qubits[2])
    circ << CNOT(qubits[2], qubits[3])
    circ << CNOT(qubits[3], qubits[4])
    return circ


def _collect_linear_blocks(max_block_width=None):
    ops = [
        ("h", [0]),
        ("cx", [0, 1]),
        ("cx", [1, 2]),
        ("cx", [2, 3]),
        ("cx", [3, 4]),
    ]

    blocks = []
    current_block = []
    current_qubits = set()

    def flush():
        if current_block:
            blocks.append((list(current_block), set(current_qubits)))

    for name, qs in ops:
        if name in ("cx", "swap") or (name == "h" and False):
            proposed = current_qubits | set(qs)
            if max_block_width is not None and len(proposed) > max_block_width and current_qubits:
                flush()
                current_block = []
                current_qubits = set()
                proposed = set(qs)
            current_block.append((name, qs))
            current_qubits = proposed
        else:
            flush()
            current_block = []
            current_qubits = set()
            blocks.append(([(name, qs)], set(qs)))

    flush()

    result_blocks = []
    for block_ops, block_q in blocks:
        if len(block_ops) == 1 and block_ops[0][0] == "h":
            result_blocks.append(("gate", block_ops[0]))
        else:
            result_blocks.append(("linear_function", block_ops, sorted(block_q)))
    return result_blocks


def collect_linear_blocks_with_and_without_limit():
    circ = _build_circuit()
    prog = QProg()
    prog << circ
    machine.directly_run(prog)

    full_block = _collect_linear_blocks(max_block_width=None)
    limited_block = _collect_linear_blocks(max_block_width=3)

    return full_block, limited_block


if __name__ == "__main__":
    fb, lb = collect_linear_blocks_with_and_without_limit()
    print(fb)
    print(lb)
    machine.finalize()
