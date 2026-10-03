# EVAL_META: task_id=119, framework=pennylane, class=3
import numpy as np
import pennylane as qml


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    n = int(num_state_qubits)
    if n < 1:
        raise ValueError("num_state_qubits must be at least 1")

    if kind == "full":
        num_qubits = 2 * n + 2
        cin = 0
        a_start = 1
        b_start = 1 + n
        cout = 2 * n + 1
    elif kind == "half":
        num_qubits = 2 * n + 1
        cin = None
        a_start = 0
        b_start = n
        cout = 2 * n
    else:
        num_qubits = 2 * n
        cin = None
        a_start = 0
        b_start = n
        cout = None

    dim = 1 << num_qubits
    unitary = np.zeros((dim, dim), dtype=complex)
    mask = (1 << n) - 1

    for col in range(dim):
        bits = [(col >> (num_qubits - 1 - i)) & 1 for i in range(num_qubits)]

        a_val = sum(bits[a_start + i] << i for i in range(n))
        b_val = sum(bits[b_start + i] << i for i in range(n))
        c_in = bits[cin] if cin is not None else 0

        total = a_val + b_val + c_in
        b_new = total & mask
        carry = (total >> n) & 1

        out_bits = bits[:]
        for i in range(n):
            out_bits[b_start + i] = (b_new >> i) & 1

        if cout is not None:
            out_bits[cout] ^= carry

        row = 0
        for bit in out_bits:
            row = (row << 1) | bit

        unitary[row, col] = 1.0

    op = qml.QubitUnitary(unitary, wires=range(num_qubits))
    return qml.tape.QuantumScript([op])
