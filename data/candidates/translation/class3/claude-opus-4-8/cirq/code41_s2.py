# EVAL_META: task_id=41, framework=cirq, class=3
import numpy as np
import cirq


def compose_op():
    dim = 2 ** 3
    op = np.eye(dim, dtype=complex)

    X = cirq.unitary(cirq.X)
    Y = cirq.unitary(cirq.Y)
    yx = np.kron(Y, X)

    embed = np.eye(dim, dtype=complex)

    def apply_on_qubits(single_two_qubit_op, qargs, num_qubits):
        full = np.zeros((dim, dim), dtype=complex)
        for i in range(dim):
            bits = [(i >> (num_qubits - 1 - q)) & 1 for q in range(num_qubits)]
            in0 = bits[qargs[0]]
            in1 = bits[qargs[1]]
            in_idx = (in1 << 1) | in0
            for out_idx in range(4):
                amp = single_two_qubit_op[out_idx, in_idx]
                if amp == 0:
                    continue
                out0 = out_idx & 1
                out1 = (out_idx >> 1) & 1
                new_bits = list(bits)
                new_bits[qargs[0]] = out0
                new_bits[qargs[1]] = out1
                j = 0
                for q in range(num_qubits):
                    j |= new_bits[q] << (num_qubits - 1 - q)
                full[j, i] += amp
        return full

    embed = apply_on_qubits(yx, [0, 2], 3)

    result = embed.dot(op)
    return result
