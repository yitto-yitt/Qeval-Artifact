# EVAL_META: task_id=86, framework=cirq, class=3
import cirq
import numpy as np


def _collect_linear_blocks(qubits, ops, max_block_width=None):
    linear_gates = (cirq.CXPowGate, cirq.CZPowGate, cirq.SwapPowGate)

    def is_linear(op):
        if isinstance(op.gate, linear_gates):
            if isinstance(op.gate, cirq.CXPowGate) and op.gate.exponent != 1:
                return False
            return True
        return False

    result_ops = []
    i = 0
    n = len(ops)
    while i < n:
        if not is_linear(ops[i]):
            result_ops.append(ops[i])
            i += 1
            continue

        block = [ops[i]]
        involved = set(ops[i].qubits)
        j = i + 1
        while j < n and is_linear(ops[j]):
            new_qubits = involved | set(ops[j].qubits)
            if max_block_width is not None and len(new_qubits) > max_block_width:
                break
            block.append(ops[j])
            involved = new_qubits
            j += 1

        if len(block) >= 1:
            block_qubits = sorted(involved)
            sub = cirq.Circuit(block)
            matrix = sub.unitary(qubit_order=block_qubits)
            gate = cirq.MatrixGate(matrix, name="LinearFunction")
            result_ops.append(gate.on(*block_qubits))
        else:
            result_ops.extend(block)
        i = j

    return cirq.Circuit(result_ops)


def collect_linear_blocks_with_and_without_limit():
    qubits = [cirq.LineQubit(i) for i in range(5)]
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
