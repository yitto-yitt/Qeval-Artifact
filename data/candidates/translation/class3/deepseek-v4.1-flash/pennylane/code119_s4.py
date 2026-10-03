# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml
import numpy as np

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in ['full', 'half', 'fixed']:
        raise ValueError("kind must be 'full', 'half', or 'fixed'")
    
    if kind == 'full':
        num_qubits = 2 * num_state_qubits + 1
    elif kind == 'half':
        num_qubits = 2 * num_state_qubits
    elif kind == 'fixed':
        num_qubits = 2 * num_state_qubits + 1
    
    dim = 2 ** num_qubits
    U = np.zeros((dim, dim), dtype=complex)
    
    for x in range(dim):
        n = num_state_qubits
        a = x & ((1 << n) - 1)
        b = (x >> n) & ((1 << n) - 1)
        if kind == 'half':
            sum_val = a + b
            b_new = sum_val & ((1 << n) - 1)
            y = a | (b_new << n)
        elif kind == 'full':
            c = (x >> (2 * n)) & 1
            sum_val = a + b + c
            b_new = sum_val & ((1 << n) - 1)
            c_new = (sum_val >> n) & 1
            y = a | (b_new << n) | (c_new << (2 * n))
        elif kind == 'fixed':
            c = (x >> (2 * n)) & 1
            if c == 0:
                sum_val = a + b
                b_new = sum_val & ((1 << n) - 1)
                y = a | (b_new << n) | (0 << (2 * n))
            else:
                y = x
        U[y, x] = 1.0
    
    ops = [qml.QubitUnitary(U, wires=range(num_qubits))]
    return qml.tape.QuantumScript(ops)
