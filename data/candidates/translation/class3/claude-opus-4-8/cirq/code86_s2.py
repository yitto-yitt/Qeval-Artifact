# EVAL_META: task_id=86, framework=cirq, class=3
import cirq
import numpy as np


def _collect_linear_blocks(qubits, ops, max_block_width=None):
    linear_gate_types = (cirq.CXPowGate, cirq.CZPowGate)

    def is_linear(op):
        g = op.gate
        if isinstance(g, cirq.CXPowGate) and g.exponent == 1:
            return True
        if isinstance(g, cirq.CZPowGate) and g.exponent == 1:
            return True
        return False

    blocks = []
    current = []
    current_qubits = set()

    def flush():
        nonlocal current, current_qubits
        if current:
            blocks.append((list(current), set(current_qubits)))
            current = []
            current_qubits = set()

    for op in ops:
        if is_linear(op):
            new_qubits = current_qubits | set(op.qubits)
            if max_block_width is not None and len(new_qubits) > max_block_width and current:
                flush()
                new_qubits = set(op.qubits)
            current.append(op)
            current_qubits = new_qubits
        else:
            flush()
            blocks.append(([op], set(op.qubits)))
    flush()

    result = cirq.Circuit()
    for block_ops, block_qubits in blocks:
        if len(block_ops) == 1 and not is_linear(block_ops[0]):
            result.append(block_ops[0])
        else:
            bq = sorted(block_qubits)
            sub = cirq.Circuit(block_ops)
            u = sub.unitary(qubit_order=bq)
            gate = cirq.MatrixGate(u)
            result.append(gate.on(*bq))
    return result


def collect_linear_blocks_with_and_without_limit():
    qubits = cirq.LineQubit.range(5)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CX(qubits[0], qubits[1]))
    circuit.append(cirq.CX(qubits[1], qubits[2]))
    circuit.append(cirq.CX(qubits[2], qubits[3]))
    circuit.append(cirq.CX(qubits[3], qubits[4]))

    ops = list(circuit.all_operations())

    full_block = _collect_linear_blocks(qubits, ops, max_block_width=None)
    limited_block = _collect_linear_blocks(qubits, ops, max_block_width=3)

    return full_block, limited_block
