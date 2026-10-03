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
        
    amplitudes = np.array(amplitudes, dtype=complex)
    n = 2**num_qubits
    
    if n == 1:
        U = np.array([[1.0]], dtype=complex)
    else:
        M = np.eye(n, dtype=complex)
        M[:, 0] = amplitudes
        Q, R = np.linalg.qr(M, mode='complete')
        Q[:, 0] *= R[0, 0]
        U = Q
        
    qubits = cirq.LineQubit.range(num_qubits)
    gate = cirq.MatrixGate(U)
    circuit = cirq.Circuit(gate(*qubits))
    return circuit
