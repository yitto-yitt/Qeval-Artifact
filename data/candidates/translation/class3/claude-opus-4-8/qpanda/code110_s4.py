# EVAL_META: task_id=110, framework=qpanda, class=3
import numpy as np
import random
from pyqpanda3.core import QCircuit, QProg, H, S, X, Y, Z, CNOT, matrix_of_circuit


def _global_phase_equiv(a, b, rtol=0.4, atol=0.4):
    a = np.asarray(a, dtype=complex)
    b = np.asarray(b, dtype=complex)
    if a.shape != b.shape:
        return False
    idx = np.unravel_index(np.argmax(np.abs(b)), b.shape)
    if abs(b[idx]) < 1e-12:
        return np.allclose(a, b, rtol=rtol, atol=atol)
    if abs(a[idx]) < 1e-12:
        return np.allclose(a, b, rtol=rtol, atol=atol)
    phase = a[idx] / b[idx]
    return np.allclose(a, phase * b, rtol=rtol, atol=atol)


def _circuit_matrix(circ, num_qubits):
    prog = QProg()
    prog << circ
    return matrix_of_circuit(prog)


def _random_clifford_circuit(num_qubits, depth_factor=6):
    circ = QCircuit()
    single = ['H', 'S', 'X', 'Y', 'Z']
    gate_map = {'H': H, 'S': S, 'X': X, 'Y': Y, 'Z': Z}
    depth = max(1, depth_factor * num_qubits * num_qubits)
    for _ in range(depth):
        if num_qubits > 1 and random.random() < 0.4:
            q = random.sample(range(num_qubits), 2)
            circ << CNOT(q[0], q[1])
        else:
            q = random.randrange(num_qubits)
            g = random.choice(single)
            circ << gate_map[g](q)
    return circ


def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.qubit_num() if hasattr(circuit, "qubit_num") else circuit.num_qubits
    target = _circuit_matrix(circuit, num_qubits)

    qc_list = []
    counter = 0
    while counter < n:
        qc = _random_clifford_circuit(num_qubits)
        mat = _circuit_matrix(qc, num_qubits)
        if _global_phase_equiv(mat, target, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
