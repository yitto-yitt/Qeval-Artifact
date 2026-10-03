# EVAL_META: task_id=86, framework=cirq, class=3
import cirq
import numpy as np


def _collect_linear_blocks(qubits, ops, max_block_width=None):
    linear_ops = {'CNOT', 'CX', 'CZ', 'SWAP'}

    def is_linear(op):
        gate = op.gate
        if isinstance(gate, cirq.CXPowGate) and gate.exponent == 1:
            return True
        if isinstance(gate, cirq.CZPowGate) and gate.exponent == 1:
            return True
        if isinstance(gate, cirq.SwapPowGate) and gate.exponent == 1:
            return True
        return False

    result = cirq.Circuit()
    n = len(ops)
    i = 0
    while i < n:
        op = ops[i]
        if not is_linear(op):
            result.append(op)
            i += 1
            continue
        block_ops = [op]
        block_qubits = set(op.qubits)
        j = i + 1
        while j < n:
            nxt = ops[j]
            if not is_linear(nxt):
                break
            new_qubits = block_qubits | set(nxt.qubits)
            if max_block_width is not None and len(new_qubits) > max_block_width:
                break
            block_ops.append(nxt)
            block_qubits = new_qubits
            j += 1
        sorted_qubits = sorted(block_qubits)
        sub = cirq.Circuit(block_ops)
        matrix = sub.unitary(qubit_order=sorted_qubits)
        result.append(cirq.MatrixGate(matrix).on(*sorted_qubits))
        i = j
    return result


def collect_linear_blocks_with_and_without_limit():
    qubits = cirq.LineQubit.range(5)
    ops = [
        cirq.H(qubits[0]),
        cirq.CNOT(qubits[0], qubits[1]),
        cirq.CNOT(qubits[1], qubits[2]),
        cirq.CNOT(qubits[2], qubits[3]),
        cirq.CNOT(qubits[3], qubits[4]),
    ]
    full_block = _collect_linear_blocks(qubits, ops, max_block_width=None)
    limited_block = _collect_linear_blocks(qubits, ops, max_block_width=3)
    return full_block, limited_block
