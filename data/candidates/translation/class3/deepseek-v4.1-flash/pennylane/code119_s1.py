# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    if kind == 'full':
        num_carry = 2
    elif kind == 'half':
        num_carry = 1
    else:  # fixed
        num_carry = 0
    N = 2 * n + num_carry

    U = np.zeros((2**N, 2**N), dtype=complex)
    for state in range(2**N):
        if kind == 'full':
            carry_in = (state >> 0) & 1
            a = 0
            for i in range(n):
                a |= ((state >> (1 + i)) & 1) << i
            b = 0
            for i in range(n):
                b |= ((state >> (n + 1 + i)) & 1) << i
            sum_val = a + b + carry_in
            b_new = sum_val & ((1 << n) - 1)
            carry_out = (sum_val >> n) & 1
            new_state = 0
            new_state |= carry_in << 0
            for i in range(n):
                new_state |= ((a >> i) & 1) << (1 + i)
            for i in range(n):
                new_state |= ((b_new >> i) & 1) << (n + 1 + i)
            new_state |= carry_out << (2 * n + 1)
        elif kind == 'half':
            a = 0
            for i in range(n):
                a |= ((state >> i) & 1) << i
            b = 0
            for i in range(n):
                b |= ((state >> (n + i)) & 1) << i
            sum_val = a + b
            b_new = sum_val & ((1 << n) - 1)
            carry_out = (sum_val >> n) & 1
            new_state = 0
            for i in range(n):
                new_state |= ((a >> i) & 1) << i
            for i in range(n):
                new_state |= ((b_new >> i) & 1) << (n + i)
            new_state |= carry_out << (2 * n)
        else:  # fixed
            a = 0
            for i in range(n):
                a |= ((state >> i) & 1) << i
            b = 0
            for i in range(n):
                b |= ((state >> (n + i)) & 1) << i
            sum_val = a + b
            b_new = sum_val & ((1 << n) - 1)
            new_state = 0
            for i in range(n):
                new_state |= ((a >> i) & 1) << i
            for i in range(n):
                new_state |= ((b_new >> i) & 1) << (n + i)
        U[new_state, state] = 1.0

    dev = qml.device('default.qubit', wires=N)
    @qml.qnode(dev)
    def circuit():
        qml.QubitUnitary(U, wires=range(N))
        return qml.state()
    return circuit
