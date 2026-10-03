# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    if kind == 'full':
        N = 2 * n + 2
    elif kind in ('half', 'fixed'):
        N = 2 * n + 1
    else:
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    dim = 1 << N
    matrix = np.zeros((dim, dim), dtype=complex)

    for x in range(dim):
        a = x & ((1 << n) - 1)
        b = (x >> n) & ((1 << n) - 1)
        if kind == 'full':
            c_in = (x >> (2 * n)) & 1
            c_out = (x >> (2 * n + 1)) & 1
        else:
            c_in = 0
            c_out = (x >> (2 * n)) & 1

        sum_val = a + b + c_in
        a_new = sum_val % (1 << n)
        carry_out = sum_val >> n
        c_out_new = c_out ^ carry_out

        y = a_new | (b << n)
        if kind == 'full':
            y |= c_in << (2 * n)
            y |= c_out_new << (2 * n + 1)
        else:
            y |= c_out_new << (2 * n)

        matrix[y, x] = 1.0

    with qml.tape.QuantumTape() as tape:
        qml.QubitUnitary(matrix, wires=list(range(N - 1, -1, -1)))
    return tape
