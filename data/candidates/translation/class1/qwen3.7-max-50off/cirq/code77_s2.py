# EVAL_META: task_id=77, framework=cirq, class=1
import math
import numpy as np
import cirq

def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))
        
    state = np.array(amplitudes, dtype=float)
    norm = np.linalg.norm(state)
    if norm > 0:
        state = state / norm
        
    n = 2**num_qubits
    e1 = np.zeros(n, dtype=float)
    e1[0] = 1.0
    
    diff = e1 - state
    norm_diff = np.linalg.norm(diff)
    if norm_diff < 1e-10:
        U = np.eye(n, dtype=complex)
    else:
        u = diff / norm_diff
        U = np.eye(n, dtype=complex) - 2 * np.outer(u, u)
        
    gate = cirq.MatrixGate(U)
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit(gate(*qubits))
    return circuit
