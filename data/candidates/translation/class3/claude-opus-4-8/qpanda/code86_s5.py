# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, H, CNOT


def collect_linear_blocks_with_and_without_limit():
    def build_base():
        circ = QCircuit(5)
        circ << H(0)
        circ << CNOT(0, 1)
        circ << CNOT(1, 2)
        circ << CNOT(2, 3)
        circ << CNOT(3, 4)
        return circ

    def collect_linear_blocks(max_block_width=None):
        gates = [
            ("h", [0]),
            ("cx", [0, 1]),
            ("cx", [1, 2]),
            ("cx", [2, 3]),
            ("cx", [3, 4]),
        ]

        blocks = []
        current = []
        current_qubits = set()

        def flush():
            nonlocal current, current_qubits
            if current:
                blocks.append(("linear", list(current), set(current_qubits)))
                current = []
                current_qubits = set()

        for name, qubits in gates:
            if name == "cx":
                candidate = set(current_qubits) | set(qubits)
                if max_block_width is not None and len(candidate) > max_block_width:
                    flush()
                current.append((name, qubits))
                current_qubits |= set(qubits)
            else:
                flush()
                blocks.append(("gate", [(name, qubits)], set(qubits)))
        flush()

        prog = QProg()
        base = build_base()
        prog << base

        collected = []
        for kind, gate_list, qubits in blocks:
            if kind == "linear" and len(gate_list) >= 1:
                collected.append(("LinearFunction", sorted(qubits), gate_list))
            else:
                collected.append((gate_list[0][0], gate_list[0][1], gate_list))
        return prog, collected

    full_block, _ = collect_linear_blocks(max_block_width=None)
    limited_block, _ = collect_linear_blocks(max_block_width=3)
    return full_block, limited_block
