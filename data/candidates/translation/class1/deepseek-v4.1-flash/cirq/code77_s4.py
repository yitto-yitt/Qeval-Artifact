# EVAL_META: task_id=77, framework=cirq, class=1
import math
import cirq
import numpy as np

def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))
    norm = math.sqrt(sum(a * a for a in amplitudes))
    if norm > 1e-12:
        amplitudes = [a / norm for a in amplitudes]
    qubits = cirq.LineQubit.range(num_qubits)
    dim = 2**num_qubits
    state = np.array(amplitudes, dtype=float)
    if abs(state[0] - 1.0) < 1e-9:
        U = np.eye(dim, dtype=float)
    else:
        v = np.zeros(dim, dtype=float)
        v[0] = 1.0
        v = v - state
        v = v / np.linalg.norm(v)
        U = np.eye(dim, dtype=float) - 2 * np.outer(v, v)
    gate = cirq.MatrixGate(U)
    circuit = cirq.Circuit(gate.on(*qubits))
    return circuit
