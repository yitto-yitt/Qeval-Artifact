# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QGate, H, CNOT


def _build_base():
    circ = QCircuit(5)
    circ << H(0)
    circ << CNOT(0, 1)
    circ << CNOT(1, 2)
    circ << CNOT(2, 3)
    circ << CNOT(3, 4)
    return circ


def _collect_linear_blocks(max_block_width=None):
    base = _build_base()
    gates = []
    for op in base.operations():
        name = op.name().upper()
        qubits = list(op.qubits())
        if name == "CNOT" or name == "CX":
            gates.append(("linear", qubits))
        else:
            gates.append(("nonlinear", qubits, name))

    blocks = []
    current = []
    current_qubits = set()

    def flush():
        if current:
            blocks.append(list(current))

    for g in gates:
        if g[0] == "linear":
            qs = g[1]
            if max_block_width is not None:
                new_qubits = current_qubits | set(qs)
                if len(new_qubits) > max_block_width and current:
                    flush()
                    current.clear()
                    current_qubits.clear()
            current.append(qs)
            current_qubits.update(qs)
        else:
            flush()
            current.clear()
            current_qubits.clear()
    flush()

    result = QCircuit(5)
    idx = 0
    gi = 0
    for g in gates:
        if g[0] == "nonlinear":
            if g[2] == "H":
                result << H(g[1][0])
            gi += 1
        else:
            gi += 1

    out = QCircuit(5)
    for g in gates:
        if g[0] == "nonlinear":
            if g[2] == "H":
                out << H(g[1][0])
        else:
            out << CNOT(g[1][0], g[1][1])

    return out, blocks


def collect_linear_blocks_with_and_without_limit():
    full_block, _ = _collect_linear_blocks(max_block_width=None)
    limited_block, _ = _collect_linear_blocks(max_block_width=3)
    return full_block, limited_block
