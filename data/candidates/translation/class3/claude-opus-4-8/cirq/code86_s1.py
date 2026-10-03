# EVAL_META: task_id=86, framework=cirq, class=3
import cirq


def _build_base_circuit():
    qubits = cirq.LineQubit.range(5)
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CX(qubits[0], qubits[1]))
    circuit.append(cirq.CX(qubits[1], qubits[2]))
    circuit.append(cirq.CX(qubits[2], qubits[3]))
    circuit.append(cirq.CX(qubits[3], qubits[4]))
    return circuit, qubits


def _is_linear(op):
    return isinstance(op.gate, type(cirq.CX)) or op.gate == cirq.CNOT


def _collect_linear_blocks(circuit, qubits, max_block_width=None):
    moments_ops = list(circuit.all_operations())
    result = cirq.Circuit()

    current_block = []
    current_qubits = set()

    def flush_block():
        nonlocal current_block, current_qubits
        if not current_block:
            return
        if len(current_block) == 1:
            result.append(current_block[0])
        else:
            block_qubits = sorted(current_qubits)
            sub = cirq.Circuit(current_block)
            gate = cirq.MatrixGate(
                cirq.unitary(sub.freeze()[: ]) if False else sub.unitary(qubit_order=block_qubits)
            )
            result.append(gate.on(*block_qubits))
        current_block = []
        current_qubits = set()

    for op in moments_ops:
        is_lin = (op.gate == cirq.CNOT) or (op.gate == cirq.CX)
        if not is_lin:
            flush_block()
            result.append(op)
            continue

        new_qubits = current_qubits | set(op.qubits)
        if max_block_width is not None and len(new_qubits) > max_block_width:
            flush_block()
            current_block = [op]
            current_qubits = set(op.qubits)
        else:
            current_block.append(op)
            current_qubits = new_qubits

    flush_block()
    return result


def collect_linear_blocks_with_and_without_limit():
    circuit_full, qubits = _build_base_circuit()
    full_block = _collect_linear_blocks(circuit_full, qubits, max_block_width=None)

    circuit_limited, qubits2 = _build_base_circuit()
    limited_block = _collect_linear_blocks(circuit_limited, qubits2, max_block_width=3)

    return full_block, limited_block
