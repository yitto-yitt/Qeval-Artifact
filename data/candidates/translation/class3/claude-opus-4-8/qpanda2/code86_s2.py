# EVAL_META: task_id=86, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, H, CNOT

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)


def _build_base_circuit():
    circ = QCircuit()
    circ << H(qubits[0])
    circ << CNOT(qubits[0], qubits[1])
    circ << CNOT(qubits[1], qubits[2])
    circ << CNOT(qubits[2], qubits[3])
    circ << CNOT(qubits[3], qubits[4])
    return circ


def _collect_linear_blocks(gates, max_block_width=None):
    linear_gate_names = {"CNOT", "CX", "SWAP", "CZ"}
    blocks = []
    current_block = []
    current_qubits = set()

    for name, qs in gates:
        if name in linear_gate_names:
            if max_block_width is not None:
                new_qubits = current_qubits | set(qs)
                if len(new_qubits) > max_block_width and current_block:
                    blocks.append(("linear", current_block))
                    current_block = []
                    current_qubits = set()
            current_block.append((name, qs))
            current_qubits |= set(qs)
        else:
            if current_block:
                blocks.append(("linear", current_block))
                current_block = []
                current_qubits = set()
            blocks.append(("gate", [(name, qs)]))

    if current_block:
        blocks.append(("linear", current_block))

    return blocks


def collect_linear_blocks_with_and_without_limit():
    gate_seq = [
        ("H", [0]),
        ("CNOT", [0, 1]),
        ("CNOT", [1, 2]),
        ("CNOT", [2, 3]),
        ("CNOT", [3, 4]),
    ]

    base_circuit = _build_base_circuit()

    full_block = _collect_linear_blocks(gate_seq, max_block_width=None)
    limited_block = _collect_linear_blocks(gate_seq, max_block_width=3)

    prog_full = machine.qAlloc_many(0) if False else None
    prog = QCircuit()
    prog << base_circuit
    machine.directly_run(machine.qAlloc_many(0) if False else _to_prog(base_circuit))

    return (full_block, limited_block)


def _to_prog(circ):
    from pyqpanda import QProg
    prog = QProg()
    prog << circ
    return prog


result = collect_linear_blocks_with_and_without_limit()
machine.finalize()
