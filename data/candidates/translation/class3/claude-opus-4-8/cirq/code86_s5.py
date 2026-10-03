# EVAL_META: task_id=86, framework=cirq, class=3
import cirq
import numpy as np


def _collect_linear_blocks(qubits, ops, max_block_width=None):
    linear_gates = {'CX', 'CZ', 'SWAP'}

    def op_qubit_indices(op, qubit_index):
        return [qubit_index[q] for q in op.qubits]

    def is_linear(op):
        gate = op.gate
        if isinstance(gate, cirq.CXPowGate) and gate.exponent == 1:
            return True
        if isinstance(gate, cirq.CZPowGate) and gate.exponent == 1:
            return True
        if isinstance(gate, cirq.SwapPowGate) and gate.exponent == 1:
            return True
        if gate == cirq.CNOT or gate == cirq.CZ or gate == cirq.SWAP:
            return True
        return False

    qubit_index = {q: i for i, q in enumerate(qubits)}

    new_ops = []
    i = 0
    n = len(ops)
    while i < n:
        op = ops[i]
        if is_linear(op):
            block = [op]
            block_qubits = set(op.qubits)
            j = i + 1
            while j < n:
                next_op = ops[j]
                if not is_linear(next_op):
                    break
                candidate_qubits = block_qubits | set(next_op.qubits)
                if max_block_width is not None and len(candidate_qubits) > max_block_width:
                    break
                block.append(next_op)
                block_qubits = candidate_qubits
                j += 1

            block_qubit_list = sorted(block_qubits, key=lambda q: qubit_index[q])
            local_index = {q: k for k, q in enumerate(block_qubit_list)}
            dim = len(block_qubit_list)
            mat = np.eye(1 << dim, dtype=complex)
            for bop in block:
                full = cirq.unitary(
                    cirq.Circuit(bop).transform_qubits(
                        {q: cirq.LineQubit(local_index[q]) for q in block_qubit_list}
                    )
                ) if False else None
            # Build combined unitary over block qubits
            sub_circuit = cirq.Circuit()
            mapping = {q: cirq.LineQubit(local_index[q]) for q in block_qubit_list}
            for bop in block:
                sub_circuit.append(bop.transform_qubits(mapping))
            block_unitary = sub_circuit.unitary(
                qubit_order=[cirq.LineQubit(k) for k in range(dim)]
            )
            new_ops.append(
                cirq.MatrixGate(block_unitary, name="LinearFunction").on(*block_qubit_list)
            )
            i = j
        else:
            new_ops.append(op)
            i += 1

    return new_ops


def collect_linear_blocks_with_and_without_limit():
    qubits = [cirq.LineQubit(i) for i in range(5)]
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    circuit.append(cirq.CNOT(qubits[1], qubits[2]))
    circuit.append(cirq.CNOT(qubits[2], qubits[3]))
    circuit.append(cirq.CNOT(qubits[3], qubits[4]))

    ops = list(circuit.all_operations())

    full_ops = _collect_linear_blocks(qubits, ops, max_block_width=None)
    limited_ops = _collect_linear_blocks(qubits, ops, max_block_width=3)

    full_block = cirq.Circuit(full_ops)
    limited_block = cirq.Circuit(limited_ops)

    return full_block, limited_block
