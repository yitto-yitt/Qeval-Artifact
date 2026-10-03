# EVAL_META: task_id=110, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, QProg, H, S, X, Y, Z, CNOT


def _circuit_unitary(circ, num_qubits):
    prog = QProg()
    prog.append(circ)
    from pyqpanda3.core import matrix_of_circuit_or_program as _m
    try:
        mat = np.array(_m(prog)).reshape((2 ** num_qubits, 2 ** num_qubits))
    except Exception:
        mat = np.array(prog.matrix()).reshape((2 ** num_qubits, 2 ** num_qubits))
    return mat


def _get_unitary(circ, num_qubits):
    try:
        return _circuit_unitary(circ, num_qubits)
    except Exception:
        pass
    try:
        mat = np.array(circ.matrix()).reshape((2 ** num_qubits, 2 ** num_qubits))
        return mat
    except Exception:
        pass
    from pyqpanda3.core import QProg as _QP
    prog = _QP()
    prog.append(circ)
    mat = np.array(prog.matrix()).reshape((2 ** num_qubits, 2 ** num_qubits))
    return mat


def _random_clifford_circuit(num_qubits, depth=None):
    if depth is None:
        depth = 4 * num_qubits + 4
    circ = QCircuit(num_qubits)
    single = ['H', 'S', 'X', 'Y', 'Z']
    for _ in range(depth):
        for q in range(num_qubits):
            g = np.random.choice(single)
            if g == 'H':
                circ << H(q)
            elif g == 'S':
                circ << S(q)
            elif g == 'X':
                circ << X(q)
            elif g == 'Y':
                circ << Y(q)
            elif g == 'Z':
                circ << Z(q)
        if num_qubits > 1:
            for _ in range(num_qubits):
                a = np.random.randint(num_qubits)
                b = np.random.randint(num_qubits)
                if a != b:
                    circ << CNOT(a, b)
    return circ


def _equiv(u1, u2, rtol=0.4, atol=0.4):
    dim = u1.shape[0]
    inner = np.trace(np.conjugate(u1.T) @ u2)
    phase = inner / dim
    if abs(abs(phase) - 1.0) > 1e-6 and abs(phase) < 1e-9:
        return False
    if abs(phase) < 1e-12:
        return False
    u2_adj = u2 * (np.conjugate(phase) / abs(phase)) if abs(phase) > 0 else u2
    return np.allclose(u1, u2_adj, rtol=rtol, atol=atol)


def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.get_qubit_number() if hasattr(circuit, "get_qubit_number") else circuit.num_qubits
    op_or = _get_unitary(circuit, num_qubits)
    qc_list = []
    counter = 0
    while counter < n:
        qc = _random_clifford_circuit(num_qubits)
        op_qc = _get_unitary(qc, num_qubits)
        if _equiv(op_qc, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
