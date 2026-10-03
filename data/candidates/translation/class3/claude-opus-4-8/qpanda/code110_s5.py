# EVAL_META: task_id=110, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, QGate, matrix_of_circuit, H, S, X, Y, Z, CNOT

def _random_clifford_circuit(num_qubits, rng):
    qc = QCircuit(num_qubits)
    depth = 4 * num_qubits + 4
    single_gates = ['H', 'S', 'X', 'Y', 'Z']
    for _ in range(depth):
        for q in range(num_qubits):
            g = single_gates[rng.integers(len(single_gates))]
            if g == 'H':
                qc << H(q)
            elif g == 'S':
                qc << S(q)
            elif g == 'X':
                qc << X(q)
            elif g == 'Y':
                qc << Y(q)
            elif g == 'Z':
                qc << Z(q)
        if num_qubits > 1:
            num_cx = rng.integers(0, num_qubits)
            for _ in range(int(num_cx)):
                a = int(rng.integers(num_qubits))
                b = int(rng.integers(num_qubits))
                if a != b:
                    qc << CNOT(a, b)
    return qc


def _circuit_matrix(circuit):
    try:
        return np.array(matrix_of_circuit(circuit))
    except Exception:
        return np.array(circuit.matrix())


def _equiv(u, v, rtol=0.4, atol=0.4):
    dim = u.shape[0]
    inner = np.vdot(u.reshape(-1), v.reshape(-1))
    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)
    if norm_u == 0 or norm_v == 0:
        return False
    phase = inner / (norm_u * norm_v)
    if abs(abs(phase) - 1) > 1e-6 and abs(phase) < 1e-9:
        return False
    if abs(phase) < 1e-12:
        return False
    global_phase = phase / abs(phase)
    return np.allclose(u * np.conj(global_phase), v, rtol=rtol, atol=atol)


def equivalent_clifford_circuit(circuit, n):
    op_or = _circuit_matrix(circuit)
    num_qubits = circuit.num_qubits() if callable(getattr(circuit, "num_qubits", None)) else circuit.num_qubits
    rng = np.random.default_rng()
    qc_list = []
    counter = 0
    while counter < n:
        qc = _random_clifford_circuit(num_qubits, rng)
        op_qc = _circuit_matrix(qc)
        if _equiv(op_qc, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
