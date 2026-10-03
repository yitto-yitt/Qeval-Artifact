# EVAL_META: task_id=77, framework=cirq, class=1
import math
import numpy as np
import cirq

def circuit_from_probability_dist(probability_dist):
    max_state = max(probability_dist.keys())
    num_qubits = math.ceil(math.log2(max_state + 1)) or 1
    
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))
        
    v = np.array(amplitudes, dtype=np.complex128)
    norm = np.linalg.norm(v)
    if norm > 0:
        v = v / norm
    else:
        v[0] = 1.0
        
    n = 2**num_qubits
    M = np.eye(n, dtype=np.complex128)
    M[:, 0] = v
    
    Q, R = np.linalg.qr(M)
    
    U = Q.copy()
    U[:, 0] = Q[:, 0] * R[0, 0]
    
    gate = cirq.MatrixGate(U)
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit(gate(*qubits))
    
    return circuit
