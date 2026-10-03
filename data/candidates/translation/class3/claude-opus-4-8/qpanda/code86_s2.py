# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QGate, H, CNOT


def _build_base_circuit():
    circ = QCircuit(5)
    circ << H(0)
    circ << CNOT(0, 1)
    circ << CNOT(1, 2)
    circ << CNOT(2, 3)
    circ << CNOT(3, 4)
    return circ


def _collect_linear_blocks(max_block_width=None):
    gates = [
        ("h", [0]),
        ("cx", [0, 1]),
        ("cx", [1, 2]),
        ("cx", [2, 3]),
        ("cx", [3, 4]),
    ]

    def is_linear(name):
        return name in ("cx", "swap", "linear")

    blocks = []
    current = []
    current_qubits = set()

    def flush():
        if current:
            blocks.append(list(current))

    for name, qubits in gates:
        if is_linear(name):
            candidate_qubits = current_qubits | set(qubits)
            if max_block_width is not None and len(candidate_qubits) > max_block_width:
                flush()
                current.clear()
                current_qubits.clear()
                current.append((name, qubits))
                current_qubits.update(qubits)
            else:
                current.append((name, qubits))
                current_qubits.update(qubits)
        else:
            flush()
            current.clear()
            current_qubits.clear()
            blocks.append([(name, qubits)])
    flush()

    result = QCircuit(5)
    for block in blocks:
        for name, qubits in block:
            if name == "h":
                result << H(qubits[0])
            elif name == "cx":
                result << CNOT(qubits[0], qubits[1])
    return result, blocks


def collect_linear_blocks_with_and_without_limit():
    _build_base_circuit()
    full_block, _ = _collect_linear_blocks(max_block_width=None)
    limited_block, _ = _collect_linear_blocks(max_block_width=3)
    return full_block, limited_block
