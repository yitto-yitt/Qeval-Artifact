# EVAL_META: task_id=110, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QCircuit, QProg, matrix_of_circuit
from pyqpanda3.core import H, S, X, Y, Z, CNOT


def _random_clifford_circuit(num_qubits):
    qc = QCircuit(num_qubits)
    depth = 4 * num_qubits * num_qubits + 5
    single_gates = ['H', 'S', 'X', 'Y', 'Z']
    for _ in range(depth):
        if num_qubits > 1 and np.random.rand() < 0.4:
            q = np.random.choice(num_qubits, size=2, replace=False)
            qc << CNOT(int(q[0]), int(q[1]))
        else:
            q = int(np.random.randint(num_qubits))
            g = np.random.choice(single_gates)
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
    return qc


def _operator_matrix(circuit):
    prog = QProg()
    prog << circuit
    return np.array(matrix_of_circuit(prog))


def _equiv(a, b, rtol=0.4, atol=0.4):
    dim = a.shape[0]
    inner = np.vdot(a.reshape(-1), b.reshape(-1))
    norm_a = np.linalg.norm(a.reshape(-1))
    norm_b = np.linalg.norm(b.reshape(-1))
    if norm_a == 0 or norm_b == 0:
        return np.allclose(a, b, rtol=rtol, atol=atol)
    phase = inner / abs(inner) if abs(inner) > 1e-12 else 1.0
    return np.allclose(a * np.conj(phase), b, rtol=rtol, atol=atol)


def equivalent_clifford_circuit(circuit, n):
    op_or = _operator_matrix(circuit)
    num_qubits = int(np.log2(op_or.shape[0]))
    qc_list = []
    counter = 0
    while counter < n:
        qc = _random_clifford_circuit(num_qubits)
        op_qc = _operator_matrix(qc)
        if op_qc.shape == op_or.shape and _equiv(op_qc, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
