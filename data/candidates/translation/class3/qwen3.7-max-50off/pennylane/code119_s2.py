# EVAL_META: task_id=119, framework=pennylane, class=3
import numpy as np
import pennylane as qml

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    
    if kind == 'full':
        total_qubits = 2 * n + 2
        cin_idx = 0
        a_idx = list(range(1, n + 1))
        b_idx = list(range(n + 1, 2 * n + 1))
        cout_idx = 2 * n + 1
        has_cin = True
        has_cout = True
    elif kind == 'half':
        total_qubits = 2 * n + 1
        a_idx = list(range(0, n))
        b_idx = list(range(n, 2 * n))
        cout_idx = 2 * n
        has_cin = False
        has_cout = True
    elif kind == 'fixed':
        total_qubits = 2 * n + 1
        cin_idx = 0
        a_idx = list(range(1, n + 1))
        b_idx = list(range(n + 1, 2 * n + 1))
        has_cin = True
        has_cout = False
    else:
        raise ValueError("Invalid kind")

    dim = 2 ** total_qubits
    matrix = np.zeros((dim, dim), dtype=np.complex128)
    
    for i in range(dim):
        bits = [(i >> q) & 1 for q in range(total_qubits)]
        
        cin_val = bits[cin_idx] if has_cin else 0
        
        a_val = 0
        for q in range(n):
            a_val |= (bits[a_idx[q]] << q)
            
        b_val = 0
        for q in range(n):
            b_val |= (bits[b_idx[q]] << q)
            
        total_sum = a_val + b_val + cin_val
        new_b_val = total_sum & ((1 << n) - 1)
        carry_out = (total_sum >> n) & 1
        
        out_bits = list(bits)
        for q in range(n):
            out_bits[b_idx[q]] = (new_b_val >> q) & 1
            
        if has_cout:
            out_bits[cout_idx] ^= carry_out
            
        out_i = 0
        for q in range(total_qubits):
            out_i |= (out_bits[q] << q)
            
        matrix[out_i, i] = 1.0

    with qml.tape.QuantumTape() as tape:
        qml.QubitUnitary(matrix, wires=list(range(total_qubits)))
        
    return tape
