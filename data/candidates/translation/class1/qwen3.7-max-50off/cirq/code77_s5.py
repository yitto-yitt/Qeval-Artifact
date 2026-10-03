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

    psi = np.array(amplitudes, dtype=float)
    e0 = np.zeros(2**num_qubits, dtype=float)
    e0[0] = 1.0
    
    if np.allclose(psi, e0):
        U = np.eye(2**num_qubits, dtype=complex)
    else:
        v = psi - e0
        v_norm_sq = np.dot(v, v)
        U = np.eye(2**num_qubits, dtype=complex) - 2 * np.outer(v, v) / v_norm_sq
        
    qubits = cirq.LineQubit.range(num_qubits)
    gate = cirq.MatrixGate(U)
    circuit = cirq.Circuit(gate(*qubits))
    return circuit
