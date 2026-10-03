# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, H, CNOT


def _collect_linear_blocks(gate_seq, num_qubits, max_block_width=None):
    blocks = []
    current_block = []
    current_qubits = set()

    def is_linear(name):
        return name in ("CX", "CNOT", "SWAP")

    for gate in gate_seq:
        name, qubits = gate[0], gate[1]
        if is_linear(name):
            new_qubits = current_qubits | set(qubits)
            if max_block_width is not None and len(new_qubits) > max_block_width:
                if current_block:
                    blocks.append(("linear", current_block))
                current_block = [gate]
                current_qubits = set(qubits)
            else:
                current_block.append(gate)
                current_qubits = new_qubits
        else:
            if current_block:
                blocks.append(("linear", current_block))
                current_block = []
                current_qubits = set()
            blocks.append(("gate", [gate]))
    if current_block:
        blocks.append(("linear", current_block))
    return blocks


def _build_prog(gate_seq, num_qubits):
    circ = QCircuit(num_qubits)
    for gate in gate_seq:
        name, qubits = gate[0], gate[1]
        if name == "H":
            circ << H(qubits[0])
        elif name in ("CX", "CNOT"):
            circ << CNOT(qubits[0], qubits[1])
    prog = QProg()
    prog << circ
    return prog


def collect_linear_blocks_with_and_without_limit():
    num_qubits = 5
    gate_seq = [
        ("H", [0]),
        ("CX", [0, 1]),
        ("CX", [1, 2]),
        ("CX", [2, 3]),
        ("CX", [3, 4]),
    ]

    full_blocks = _collect_linear_blocks(gate_seq, num_qubits, max_block_width=None)
    limited_blocks = _collect_linear_blocks(gate_seq, num_qubits, max_block_width=3)

    full_prog = _build_prog(gate_seq, num_qubits)
    limited_prog = _build_prog(gate_seq, num_qubits)

    return (full_prog, full_blocks), (limited_prog, limited_blocks)
